from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_ssm as ssm,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    aws_events as events,
    aws_events_targets as targets,
    RemovalPolicy,
)
from constructs import Construct


class CrawlingBatchStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """
        DynamoDB
        """
        table = dynamodb.Table(
            self, 'CrawlingPropertyCache',
            partition_key={'name': 'PropertyID', 'type': dynamodb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY
        )

        '''
        Lambda
        '''
        # Lambda Layer
        crawling_layer = _lambda.LayerVersion(
            self, 'CrawlingModuleLayer',
            code=_lambda.Code.from_asset('./lambda/layer/crawling_layer'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description='Crawling Module Layer'
        )
        common_layer = _lambda.LayerVersion(
            self, 'SlackCommonLayer',
            code=_lambda.Code.from_asset('./lambda/layer/common_layer'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description='A layer that contains the common functions.'
        )

        # Parameter Storeから各種パラメータ取得
        slack_webhook_url = ssm.StringParameter.from_string_parameter_attributes(
            self, 'SlackWebhookURL',
            parameter_name='/crawling-houses/slack/webhook/url'
        )
        spreadsheet_id = ssm.StringParameter.from_string_parameter_attributes(
            self, 'SpreadsheetID',
            parameter_name='/crawling-houses/spreadsheet/id'
        )

        crawling_lambda = _lambda.Function(
            self, 'CrawlingHandler',
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler='handler.lambda_handler',
            code=_lambda.Code.from_asset('./lambda/crawling_batch'),
            timeout=Duration.seconds(200),
            layers=[
                crawling_layer,
                common_layer
            ],
            environment={
                'SLACK_WEBHOOK_URL': slack_webhook_url.string_value,
                'SPREADSHEET_ID': spreadsheet_id.string_value,
                'TARGET_SLACK_CHANNEL': '#crawler-property',
                'TARGET_SHEET_NAME': 'Crawler Property Results',
                'DYNAMODB_TABLE_NAME': table.table_name,
            }
        )

        '''
        EventBridge Rule
        '''
        rule = events.Rule(
            self, 'DailyCrawlingRule',
            schedule=events.Schedule.cron(minute='0', hour='9')  # 午前9時と午後9時に実行
        )

        # EventBridgeルールにLambdaをターゲットとして設定
        rule.add_target(targets.LambdaFunction(crawling_lambda))

        """
        Permissions
        """
        table.grant_read_write_data(crawling_lambda)

        crawling_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=['ssm:GetParameter'],
                resources=[
                    f'arn:aws:ssm:{self.region}:{self.account}:parameter/crawling-houses/google/credentials'
                ]
            )
        )

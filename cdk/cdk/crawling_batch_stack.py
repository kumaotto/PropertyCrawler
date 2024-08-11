from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_ssm as ssm,
    aws_iam as iam,
)
from constructs import Construct


class CrawlingBatchStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        '''
        Lambda
        '''
        # Lambda Layer
        scrapy_layer = _lambda.LayerVersion(
            self, 'ScrapyModuleLayer',
            code=_lambda.Code.from_asset('./lambda/layer/scrapy_layer'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description='Scrapy Module Layer'
        )

        c_packages_layer = _lambda.LayerVersion.from_layer_version_arn(
            self, 'CPackagesLayer',
            layer_version_arn='arn:aws:lambda:ap-northeast-1:024668304519:layer:c_packages:1'
        )

        # Parameter Storeから各種パラメータ取得
        slack_token = ssm.StringParameter.from_string_parameter_attributes(
            self, 'SlackToken',
            parameter_name='/crawling-houses/slack/token'
        )

        scrapy_lambda = _lambda.Function(
            self, 'ScrapyHandler',
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler='handler.lambda_handler',
            code=_lambda.Code.from_asset('./lambda/crawling_batch'),
            timeout=Duration.seconds(200),
            layers=[
                scrapy_layer,
                c_packages_layer
            ],
            environment={
                'SLACK_BOT_TOKEN': slack_token.string_value,
                'TARGET_SLACK_CHANNEL': '#crawler-property',
                'TARGET_SHEET_NAME': 'Crawler Property Results'
            }
        )

        scrapy_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=['ssm:GetParameter'],
                resources=[
                    f'arn:aws:ssm:{self.region}:{self.account}:parameter/crawling-houses/google/credentials'
                ]
            )
        )

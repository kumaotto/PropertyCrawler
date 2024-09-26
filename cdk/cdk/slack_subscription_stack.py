from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_ssm as ssm,
    aws_iam as iam,
    aws_lambda_python_alpha as lambda_alpha,
)
from constructs import Construct


class SlackSubscriptionStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """
        Lambda
        """
        # Parameter Storeから各種パラメータ取得
        slack_token = ssm.StringParameter.from_string_parameter_attributes(
            self, "SlackToken", parameter_name="/crawling-houses/slack/token"
        )
        spreadsheet_id = ssm.StringParameter.from_string_parameter_attributes(
            self, "SpreadsheetId", parameter_name="/crawling-houses/spreadsheet/id"
        )

        # Lambda Layer
        module_layer = lambda_alpha.PythonLayerVersion(
            self,
            "SlackModuleLayer",
            entry="lambda/layer/modules_layer",
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description="A layer that contains the Slack client.",
        )

        common_layer = lambda_alpha.PythonLayerVersion(
            self,
            "SlackCommonLayer",
            entry="lambda/layer/common_layer",
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description="A layer that contains the common functions.",
        )

        lambda_power_tool_layer = _lambda.LayerVersion.from_layer_version_arn(
            self,
            "LambdaPowerToolsLayer",
            f"arn:aws:lambda:{self.region}:017000801446:layer:AWSLambdaPowertoolsPythonV2:78",
        )

        slack_lambda = _lambda.Function(
            self,
            "SlackHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("./lambda/slack_subscription"),
            timeout=Duration.seconds(15),
            layers=[module_layer, common_layer, lambda_power_tool_layer],
            environment={
                "SLACK_BOT_TOKEN": slack_token.string_value,
                "SPREADSHEET_ID": spreadsheet_id.string_value,
            },
        )

        """
        API Gateway
        """
        api = apigateway.RestApi(
            self,
            "SlackApi",
            rest_api_name="Slack Integration API",
            description="This service handles Slack reactions.",
        )

        slack_integration = api.root.add_resource("slack")
        slack_events = slack_integration.add_resource("events")
        slack_events.add_method("POST", apigateway.LambdaIntegration(slack_lambda))

        """
        Permissions
        """
        slack_token.grant_read(slack_lambda)

        slack_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ssm:GetParameter"],
                resources=[
                    f"arn:aws:ssm:{self.region}:{self.account}:parameter/crawling-houses/google/credentials"
                ],
            )
        )

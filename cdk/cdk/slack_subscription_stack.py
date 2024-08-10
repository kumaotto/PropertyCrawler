from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_ssm as ssm,
)
from constructs import Construct


class SlackSubscriptionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Parameter StoreからSlackトークンを取得
        slack_token = ssm.StringParameter.from_string_parameter_attributes(
            self, 'SlackToken',
            parameter_name='/crawling-houses/slack/token'
        )

        """
        Lambda
        """
        slack_lambda = _lambda.Function(
            self, "SlackHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.handler",  # 既存のlambda_function.pyを使用
            code=_lambda.Code.from_asset("./lambda/slack_subscription"),
            environment={
                'SLACK_BOT_TOKEN': slack_token.string_value
            }
        )

        """
        API Gateway
        """
        api = apigateway.RestApi(
            self, "SlackApi",
            rest_api_name="Slack Integration API",
            description="This service handles Slack reactions."
        )

        slack_integration = api.root.add_resource("slack")
        slack_events = slack_integration.add_resource("events")
        slack_events.add_method("POST", apigateway.LambdaIntegration(slack_lambda))

        """
        Permissions
        """
        slack_token.grant_read(slack_lambda)

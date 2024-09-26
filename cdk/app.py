import aws_cdk as cdk

from cdk.crawling_batch_stack import CrawlingBatchStack
from cdk.slack_subscription_stack import SlackSubscriptionStack


app = cdk.App()

is_use_spreadsheet = app.node.try_get_context("isUseSpreadSheet")

SlackSubscriptionStack(app, "SlackSubscriptionStack", is_use_spreadsheet=is_use_spreadsheet)
CrawlingBatchStack(app, "CrawlingBatchStack", is_use_spreadsheet=is_use_spreadsheet)

app.synth()

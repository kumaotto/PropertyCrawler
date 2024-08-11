import aws_cdk as cdk

from cdk.crawling_batch_stack import CrawlingBatchStack
from cdk.slack_subscription_stack import SlackSubscriptionStack


app = cdk.App()
SlackSubscriptionStack(app, "SlackSubscriptionStack")
CrawlingBatchStack(app, "CrawlingBatchStack")

app.synth()

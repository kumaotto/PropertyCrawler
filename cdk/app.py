import aws_cdk as cdk

from cdk.slack_subscription_stack import SlackSubscriptionStack


app = cdk.App()
SlackSubscriptionStack(app, "SlackSubscriptionStack")

app.synth()

import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

# Slack APIクライアントの初期化
slack_token = os.environ['SLACK_BOT_TOKEN']
client = WebClient(token=slack_token)


def lambda_handler(event, context):
    try:
        # Slackのイベントデータを取得
        reaction_event = json.loads(event['body'])['event']

        if reaction_event['reaction'] == '+1':
            channel_id = reaction_event['item']['channel']
            timestamp = reaction_event['item']['ts']
            user_id = reaction_event['user']
            print('channel_id:', channel_id)
            print('stamp:', timestamp)
            print('user_id:', user_id)

            # メッセージをピンに追加
            try:
                _ = client.pins_add(
                    channel=channel_id,
                    timestamp=timestamp
                )
                print(f"Message pinned successfully in channel {channel_id}.")

            except SlackApiError as e:
                print(f"Error pinning message: {e.response['error']}")

            return {
                'statusCode': 200,
                'body': json.dumps('Reaction processed successfully')
            }

    except Exception as e:
        print(f"Error processing event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing event')
        }

import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

slack_token = os.environ['SLACK_BOT_TOKEN']
client = WebClient(token=slack_token)


def lambda_handler(event, context):

    try:
        body = json.loads(event['body'])
        print('body:', body)

        # slackのチャレンジリクエスト用
        if 'challenge' in body:
            return {
                'statusCode': 200,
                'body': body['challenge']
            }

        if 'event' in body:
            event_data = body['event']

            # 👍リアクションが追加された場合は、ピン留めする
            if event_data['reaction'] == '+1' and event_data['type'] == 'reaction_added':

                channel_id = event_data['item']['channel']
                timestamp = event_data['item']['ts']

                try:
                    _ = client.pins_add(
                        channel=channel_id,
                        timestamp=timestamp
                    )

                except SlackApiError as e:
                    print(f"Error pinning message: {e.response['error']}")

            # 👍リアクションが削除された場合は、ピン留めから削除する
            if event_data['reaction'] == '+1' and event_data['type'] == 'reaction_removed':
                channel_id = event_data['item']['channel']
                timestamp = event_data['item']['ts']

                try:
                    _ = client.pins_remove(
                        channel=channel_id,
                        timestamp=timestamp
                    )

                except SlackApiError as e:
                    print(f"Error pinning message: {e.response['error']}")

    except Exception as e:
        print(f"Error processing event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing event')
        }

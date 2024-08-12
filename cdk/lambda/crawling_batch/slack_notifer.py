import requests
import os


def send_to_slack(properties):
    slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')

    for prop in properties:

        # Slackに送信するメッセージのフォーマット
        message = (
            f"*{prop.get('title', 'N/A')}*\n"
            f"*最寄り駅:* {prop.get('station', 'N/A')}\n"
            f"*住所:* {prop.get('address', 'N/A')}\n"
            f"*階層:* {prop.get('floor', 'N/A')} / {prop.get('all_floor', 'N/A')}\n"
            f"*面積:* {prop.get('area', 'N/A')}\n"
            f"*家賃:* {prop.get('rent', 'N/A')}(管理費: {prop.get('management_fee', 'N/A')})\n"
            f"*敷金/礼金:* {prop.get('security_deposit', 'N/A')} / {prop.get('reikin', 'N/A')}\n"
            f"*築年数:* {prop.get('age', 'N/A')}\n"
            f"*URL:* {prop.get('url', 'N/A')}\n"
            f"(画像: {prop.get('image_url', 'N/A')})"
        )

        # Slackにメッセージを送信
        response = requests.post(slack_webhook_url, json={'text': message})

        # Slackへの送信が成功したかどうかを確認
        if response.status_code != 200:
            print(f"Error posting to Slack: {response.status_code}, {response.text}")

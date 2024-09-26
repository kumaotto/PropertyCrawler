import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from aws_lambda_powertools import Logger
import os
from ssm import setup_google_sheets_client
from utils import extract_property_id

# Slack設定
slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)

# スプレッドシート設定
sheet_client = setup_google_sheets_client()

SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
SHEET_NAME = "crawling"

logger = Logger()


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        logger.info("body:", body)

        # slackのチャレンジリクエスト用
        if "challenge" in body:
            return {"statusCode": 200, "body": body["challenge"]}

        if "event" in body:
            event_data = body["event"]
            channel_id = event_data["item"]["channel"]
            timestamp = event_data["item"]["ts"]
            reaction = event_data["reaction"]
            event_type = event_data["type"]

            # 👍リアクションが追加された場合
            if reaction == "+1" and event_type == "reaction_added":
                logger.info("👍リアクションが追加されました")
                add_pins(channel_id, timestamp)
                update_row_color(channel_id, timestamp, hightlight=True)

            # 👍リアクションが削除された場合
            if reaction == "+1" and event_type == "reaction_removed":
                logger.info("👍リアクションが削除されました")
                remove_pins(channel_id, timestamp)
                update_row_color(channel_id, timestamp, hightlight=False)

    except Exception:
        logger.exception("Error processing event")

    finally:
        # 常に200 OKを返すことで、Slackによるリトライを防止
        return {"statusCode": 200, "body": ""}


def add_pins(channel_id: str, timestamp: str):
    try:
        _ = client.pins_add(channel=channel_id, timestamp=timestamp)
    except SlackApiError:
        logger.exception("Error processing add_pins")


def remove_pins(channel_id: str, timestamp: str):
    try:
        _ = client.pins_remove(channel=channel_id, timestamp=timestamp)

    except SlackApiError:
        logger.exception("Error processing remove_pins")


def update_row_color(channel_id: str, timestamp: str, hightlight: bool = True):
    try:
        # 物件URLをメッセージから抽出
        response = client.conversations_history(
            channel=channel_id, latest=timestamp, inclusive=True, limit=1
        )
        message_text = response["messages"][0]["text"]
        property_URL = extract_property_id(message_text)

        if not property_URL:
            logger.error("Property URL not found in the message.")
            return

        # スプレッドシートで物件IDを検索
        sheet = sheet_client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
        cell = sheet.find(property_URL)

        if not cell:
            logger.error(f"Property ID {property_URL} not found in the sheet.")
            return

        row_number = cell.row

        # 行の色を変更
        if hightlight:
            sheet.format(
                f"A{row_number}:Z{row_number}",
                {"backgroundColor": {"red": 1.0, "green": 1.0, "blue": 0.0}},
            )
        else:
            sheet.format(
                f"A{row_number}:Z{row_number}",
                {"backgroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}},
            )

    except Exception:
        logger.exception("Error processing update_row_color")

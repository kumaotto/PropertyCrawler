import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()


class SlackPipeline:

    def __init__(self):
        token = os.getenv('SLACK_BOT_TOKEN')
        if not token:
            raise ValueError("SLACK_BOT_ACCESS_TOKEN environment variable not set")
        self.client = WebClient(token=token)

    def process_item(self, item, spider):
        message = (
            f"*{item.get('title', 'N/A')}*\n"
            f"*最寄り駅:* {item.get('station', 'N/A')}\n"
            f"*住所:* {item.get('address', 'N/A')}\n"
            f"*階層:* {item.get('floor', 'N/A')} / {item.get('all_floor', 'N/A')}\n"
            f"*面積:* {item.get('area', 'N/A')}\n"
            f"*家賃:* {item.get('rent', 'N/A')}(管理費: {item.get('management_fee', 'N/A')})\n"
            f"*敷金/礼金:* {item.get('security_deposit', 'N/A')} / {item.get('reikin', 'N/A')}\n"
            f"*築年数:* {item.get('age', 'N/A')}\n"
            f"*URL:* {item.get('url', 'N/A')}\n"
            f"(画像: {item.get('image_url', 'N/A')})"
        )

        try:
            _ = self.client.chat_postMessage(
                channel=os.getenv('TARGET_SLACK_CHANNEL'),
                text=message
            )
        except SlackApiError as e:
            spider.logger.error(f"Error posting to Slack: {e.response['error']}")

        return item


class GoogleSpreadsheetPipeline:
    def open_spider(self, spider):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_path = os.path.join(os.path.dirname(__file__), '../../credentials.json')
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        self.client = gspread.authorize(creds)

        try:
            sheet_name = os.getenv('TARGET_SLACK_CHANNEL')
            self.sheet = self.client.open(sheet_name).sheet1

        except gspread.exceptions.SpreadsheetNotFound:
            spider.logger.error("Spreadsheet not found. Please check the name and sharing settings.")
            raise

    def process_item(self, item, spider):
        self.sheet.append_row([
            item.get('url', 'URL'),
            item.get('title', 'タイトル'),
            item.get('image_url', '画像'),
            item.get('rent', '家賃'),
            item.get('management_fee', '管理費'),
            item.get('security_deposit', '敷金'),
            item.get('reikin', '礼金'),
            item.get('age', '築年数'),
            item.get('address', '住所'),
            item.get('station', '最寄り'),
            item.get('floor', '階数'),
            item.get('all_floor', '建物全体の階数'),
            item.get('area', '面積')
        ])
        return item

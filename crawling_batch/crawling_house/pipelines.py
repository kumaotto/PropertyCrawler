from datetime import datetime
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from scrapy.exceptions import DropItem

# .envファイルを読み込む
load_dotenv()


class SlackPipeline:

    def __init__(self):
        self.client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
        self.posted_urls = set()

    def process_item(self, item, spider):

        # 重複アイテムは処理をスキップ
        if item['url'] in self.posted_urls:
            spider.logger.info(f"Duplicate item skipped for Slack: {item['url']}")
            return item

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
            self.posted_urls.add(item['url'])

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
            sheet_name = os.getenv('TARGET_SHEET_NAME')
            self.sheet = self.client.open(sheet_name).sheet1

            # スプレッドシートからすでに存在するURLを読み込む
            existing_data = self.sheet.get_all_values()
            self.existing_urls = {row[0] for row in existing_data if row}

        except gspread.exceptions.SpreadsheetNotFound:
            spider.logger.error("Spreadsheet not found. Please check the name and sharing settings.")
            raise

    def process_item(self, item, spider):

        # 重複チェック
        if item['url'] in self.existing_urls:
            raise DropItem(f"Duplicate item found: {item['url']}")

        else:
            # URLリストを更新
            self.existing_urls.add(item['url'])

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.sheet.append_row([
                now,
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

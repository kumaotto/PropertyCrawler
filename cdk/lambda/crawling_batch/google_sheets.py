from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import os

from ssm import get_credentials_from_parameter_store


def send_to_sheets(properties):
    # Google Sheets APIの認証
    creds_dict = get_credentials_from_parameter_store()
    credentials = Credentials.from_service_account_info(creds_dict)
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    spreadsheet_id = os.getenv('SPREADSHEET_ID')
    range_name = 'crawling!A1'

    # スプレッドシートに追加するデータを準備
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    values = [[
        now,
        prop.get('url', 'URL'),
        prop.get('title', 'タイトル'),
        prop.get('image_url', '画像'),
        prop.get('rent', '家賃'),
        prop.get('management_fee', '管理費'),
        prop.get('security_deposit', '敷金'),
        prop.get('reikin', '礼金'),
        prop.get('age', '築年数'),
        prop.get('address', '住所'),
        prop.get('station', '最寄り'),
        prop.get('floor', '階数'),
        prop.get('all_floor', '建物全体の階数'),
        prop.get('area', '面積')
    ] for prop in properties]

    # スプレッドシートにデータを追加
    body = {'values': values}
    sheet.values().append(spreadsheetId=spreadsheet_id, range=range_name, valueInputOption='RAW', body=body).execute()

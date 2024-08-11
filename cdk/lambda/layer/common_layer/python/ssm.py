import json
import boto3
from oauth2client.service_account import ServiceAccountCredentials
import gspread


# Parameter Storeから認証情報を取得
def get_credentials_from_parameter_store():
    ssm_client = boto3.client('ssm')
    parameter_name = "/crawling-houses/google/credentials"

    try:
        parameter = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
        credentials_json = parameter['Parameter']['Value']
        return json.loads(credentials_json)
    except Exception as e:
        raise Exception(f"Error retrieving credentials from Parameter Store: {str(e)}")


# Google Sheets APIのクライアント設定
def setup_google_sheets_client():
    creds_json = get_credentials_from_parameter_store()
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
    return gspread.authorize(creds)

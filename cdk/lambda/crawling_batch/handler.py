import os
from slack_notifer import send_to_slack
from google_sheets import send_to_sheets
from cache import check_cache, update_cache
from scraper import scrape_properties

SPREADSHEET_USE_FLAG = os.environ.get("IS_USE_SPREADSHEET")


def lambda_handler(event, context):
    initial_url = event.get("url")
    properties = scrape_properties(initial_url)
    new_properties = []

    if not properties:
        print("No properties found.")
        return {"statusCode": 200, "body": "No properties to process"}

    print("properties:", properties)

    for prop in properties:
        if not check_cache(prop.get("url")):
            new_properties.append(prop)
            update_cache(prop.get("url"))

    if new_properties:
        send_to_slack(new_properties)

        if SPREADSHEET_USE_FLAG == "true":
            send_to_sheets(new_properties)

    else:
        print("No new properties to send.")

    return {"statusCode": 200, "body": "Execution complete"}

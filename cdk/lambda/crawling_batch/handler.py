from slack_notifer import send_to_slack
from google_sheets import send_to_sheets
from cache import check_cache, update_cache
from scraper import scrape_properties


def lambda_handler(event, context):
    properties = scrape_properties()
    new_properties = []

    for prop in properties:
        if not check_cache(prop['id']):
            new_properties.append(prop)
            update_cache(prop['id'])

    if new_properties:
        send_to_sheets(new_properties)
        send_to_slack(new_properties)

    return {'statusCode': 200, 'body': 'Execution complete'}

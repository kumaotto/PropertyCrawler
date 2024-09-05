from slack_notifer import send_to_slack
from google_sheets import send_to_sheets
from cache import check_cache, update_cache
from scraper import scrape_properties


def lambda_handler(event, context):

    initial_url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&ta=13&bs=040&ekInput=20110&tj=60&nk=-1&ct=14.0&cb=0.0&co=1&md=07&md=08&md=09&md=10&kz=1&ts=1&ts=3&et=10&mt=9999999&mb=0&cn=20&tc=0401303&tc=0400101&tc=0400103&tc=0400301&tc=0400901&tc=0400905&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&pc=30'
    properties = scrape_properties(initial_url)
    new_properties = []

    if not properties:
        print("No properties found.")
        return {'statusCode': 200, 'body': 'No properties to process'}

    print('properties:', properties)

    for prop in properties:
        if not check_cache(prop.get('url')):
            new_properties.append(prop)
            update_cache(prop.get('url'))

    if new_properties:
        send_to_sheets(new_properties)
        send_to_slack(new_properties)
    else:
        print("No new properties to send.")

    return {'statusCode': 200, 'body': 'Execution complete'}

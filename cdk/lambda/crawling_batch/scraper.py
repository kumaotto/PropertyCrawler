import requests
from bs4 import BeautifulSoup


def scrape_properties():
    url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&cb=0.0&ct=15.0&mb=0&mt=9999999&md=07&md=08&md=09&md=10&ts=1&ts=3&et=10&cn=20&kz=1&tc=0400103&tc=0400901&shkr1=03&shkr2=03&shkr3=03&shkr4=03&ekInput=20110&nk=-1&tj=50&sngz=&po1=09'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    properties = []
    for post in soup.select('.cassetteitem'):
        detail_url = post.select_one('a.js-cassette_link_href')['href']

        properties.append({
            'url': response.urljoin(detail_url) if detail_url else None,
            'title': post.select_one('.cassetteitem_content-title').get_text(strip=True),
            'image_url': post.select_one('img.js-noContextMenu.js-linkImage.js-adjustImg')['rel'],
            'rent': post.select_one('span.cassetteitem_other-emphasis.ui-text--bold').get_text(strip=True),
            'management_fee': post.select_one('span.cassetteitem_price.cassetteitem_price--administration').get_text(strip=True),
            'security_deposit': post.select_one('span.cassetteitem_price.cassetteitem_price--deposit').get_text(strip=True),
            'reikin': post.select_one('span.cassetteitem_price.cassetteitem_price--gratuity').get_text(strip=True),
            'age': post.select_one('li.cassetteitem_detail-col3 div:nth-child(1)').get_text(strip=True),
            'address': post.select_one('li.cassetteitem_detail-col1').get_text(strip=True),
            'station': post.select_one('li.cassetteitem_detail-col2 .cassetteitem_detail-text:nth-of-type(1)').get_text(strip=True),
            'floor': post.select_one('tr.js-cassette_link td:nth-child(3)').get_text(strip=True),
            'all_floor': post.select_one('li.cassetteitem_detail-col3 div:nth-child(2)').get_text(strip=True),
            'area': post.select_one('span.cassetteitem_menseki').get_text(strip=True),
        })

    return properties

# def scrape_properties(url):
#     properties = []

#     while url:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')

#         for post in soup.select('.cassetteitem'):
#             detail_url = post.select_one('a.js-cassette_link_href')['href']

#             properties.append({
#                 'url': response.urljoin(detail_url) if detail_url else None,
#                 'title': post.select_one('.cassetteitem_content-title').get_text(strip=True),
#                 'image_url': post.select_one('img.js-noContextMenu.js-linkImage.js-adjustImg')['rel'],
#                 'rent': post.select_one('span.cassetteitem_other-emphasis.ui-text--bold').get_text(strip=True),
#                 'management_fee': post.select_one('span.cassetteitem_price.cassetteitem_price--administration').get_text(strip=True),
#                 'security_deposit': post.select_one('span.cassetteitem_price.cassetteitem_price--deposit').get_text(strip=True),
#                 'reikin': post.select_one('span.cassetteitem_price.cassetteitem_price--gratuity').get_text(strip=True),
#                 'age': post.select_one('li.cassetteitem_detail-col3 div:nth-child(1)').get_text(strip=True),
#                 'address': post.select_one('li.cassetteitem_detail-col1').get_text(strip=True),
#                 'station': post.select_one('li.cassetteitem_detail-col2 .cassetteitem_detail-text:nth-of-type(1)').get_text(strip=True),
#                 'floor': post.select_one('tr.js-cassette_link td:nth-child(3)').get_text(strip=True),
#                 'all_floor': post.select_one('li.cassetteitem_detail-col3 div:nth-child(2)').get_text(strip=True),
#                 'area': post.select_one('span.cassetteitem_menseki').get_text(strip=True),
#             })

#         # 次のページがあるかチェック
#         next_page_tag = soup.select_one('.pagination-parts a[rel="next"]')

#         if next_page_tag:
#             next_page_url = response.urljoin(next_page_tag['href'])

#             # もし次のページのURLが現在のURLと同じならば無限ループを防ぐために終了
#             if next_page_url == url:
#                 print("Detected potential infinite loop. Exiting.")
#                 break

#             url = next_page_url
#         else:
#             # 次のページがない場合、ループを終了
#             url = None

#     return properties


# # 最初のページのURLを渡してスクレイピングを開始
# initial_url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&cb=0.0&ct=15.0&mb=0&mt=9999999&md=07&md=08&md=09&md=10&ts=1&ts=3&et=10&cn=20&kz=1&tc=0400103&tc=0400901&shkr1=03&shkr2=03&shkr3=03&shkr4=03&ekInput=20110&nk=-1&tj=50&sngz=&po1=09'
# all_properties = scrape_properties(initial_url)

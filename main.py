import requests
from bs4 import BeautifulSoup
import json
from time import sleep


headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}

def get_page_url(url, headers):
    print('Start parsing goods urls...')
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.text, 'lxml')
    page_count = int(soup.find('ul', class_='pagination').find_all('li')[-1].text.strip(']\n['))
    url_list = []
    for pn in range(1, page_count + 1):
    # for pn in range(1, 2):
        r = requests.get(url=f'https://www.rutronik24.com/pgm/molex/connectors/conn/{pn}.html')
        soup = BeautifulSoup(r.text, 'lxml')
        goods_list = soup.find_all('h2', class_='oc_herstellerartnr')

        for good in goods_list:
            good_url = good.find('a').get('href')
            url_list.append(good_url)

        print(f'Page {pn}/{page_count}')

    get_data(url_list, headers)


def get_data(list, headers):
    print('Start parsing goods info...')
    finish_data = []
    for item, url in enumerate(list):

        r = requests.get(url, headers)
        soup = BeautifulSoup(r.text, 'lxml')

        try:
            section_path_list = soup.find('ol', class_='breadcrumb hidden-print').find_all('li')
            section_path = ''
            for i in range(2, len(section_path_list)):
                section_path = section_path + '/' + section_path_list[i].text
        except Exception as ex:
            section_path = None
            print(url)
            print(ex)
        try:
            brand = soup.find('a', class_='highlight').text
        except Exception as ex:
            brand = None
            print(url)
            print(ex)
        try:
            info_list = soup.find('div', class_='col-xs-12 col-sm-5').find_all('meta')
        except Exception as ex:
            info_list = None
            print(url)
            print(ex)
        try:
            brand_article = info_list[2].get('content')
        except Exception as ex:
            brand_article = None
            print(url)
            print(ex)
        try:
            rutronic_article = info_list[3].get('content')
        except Exception as ex:
            rutronic_article = None
            print(url)
            print(ex)
        try:
            title = soup.find('div', class_='col-xs-12 col-sm-5').find('span').text.strip()
        except Exception as ex:
            title = None
            print(url)
            print(ex)
        try:
            unit_price = float(soup.find('span', class_='occalc_loading').text.strip().replace(',', '.'))
        except Exception as ex:
            unit_price = None
            print(url)
            print(ex)
        try:
            unit_pack = int(soup.find('div', class_='col-xs-12 col-sm-5').find_all('span')[4].next_sibling.text.strip())
        except Exception as ex:
            unit_pack = None
            print(url)
            print(ex)
        try:
            min_order = int(soup.find('div', class_='col-xs-12 col-sm-5').find_all('span')[5].next_sibling.text.strip())
        except Exception as ex:
            min_order = None
            print(url)
            print(ex)

        data_dict = {
            'section_path':section_path,
            'brand':brand,
            'brand_article':brand_article,
            'rutronic-article':rutronic_article,
            'title':title,
            'unit_price':unit_price,
            'unit_pack':unit_pack,
            'min_order':min_order
        }

        finish_data.append(data_dict)
        if item % 50 == 0:
            sleep(2)
            print(f'{round((item * 100 )/ len(list))}%')

    with open('results.json', 'w', encoding='utf-8') as file:
        json.dump(finish_data, file, indent=4, ensure_ascii=False)






def main():
    url = 'https://www.rutronik24.com/pgm/molex/connectors/conn/'
    get_page_url(url=url, headers=headers)


if __name__ == '__main__':
    main()
from multiprocessing import Pool
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('table', id='currencies-all').find_all('td',
                                                           class_='currency-name')
    links = []
    counter = 1
    for td in tds:
        a = td.find('a', class_='currency-name-container').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)
        counter = counter+1
        if counter == 5:
            break
    return links


def text_before_word(text, word):
    line = text.split(word)[0].strip()
    return line


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = text_before_word(soup.find('title').text, 'price')
    except:
        name = ''
    try:
        price = text_before_word(
            soup.find('span', class_='h2 text-semi-bold details-panel-item--price__value').text, 'USD')
    except:
        price = 'не нашло'
    data = {'name': name,
            'price': price}
    return data


def write_csv(data):
    with open('coinmarketcap.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'],
                         data['price']))
        print(data['name'], data['price'], 'parsed')


def make_all(link):
    html = get_html(link)
    data = get_page_data(html)
    write_csv(data)


def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/all/views/all'
    all_links = get_all_links(get_html(url))

    with Pool(40) as p:
        p.map(make_all, all_links)

    end = datetime.now()
    total = end - start
    print(str(total))
    a = input()


if __name__ == '__main__':
    main()

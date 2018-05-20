import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pymongo
from multiprocessing import Pool
import openpyxl

client = pymongo.MongoClient('localhost')
db = client['doubanddianying']

def get_one_page(page):
    url = 'https://movie.douban.com/top250?' + 'start=' + str(25*page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    }
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None

def parse_page(html):
    soup = BeautifulSoup(html, 'lxml')
    targets = soup.select('#content .article .grid_view li')
    for item in targets:
        messages = item.select('.item .info .bd p')[0].get_text().strip().split('\n')
        yield  {
            'rank': item.select('.item .pic em')[0].get_text(),
            'title':item.select('.item .info .hd a span')[0].get_text(),
            'messages': messages[0].strip() + messages[1].strip()
        }

def save_to_mongdb(content):
    try:
        if db['movies'].insert(content):
            print('存储到mongodb成功！', content)
    except Exception:
        print('存储到mongodb失败！', content)

def main(page):
    for page in range(page):
        html = get_one_page(page)
        for each in parse_page(html):
            save_to_mongdb(each)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i for i in range(10)])

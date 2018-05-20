import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import openpyxl

def get_one_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Referer':'https://www.baidu.com/link?url=BO_E3fiaOWE3zoOnhVEHKl7AJuNJ96x6hb8yJmCvGYdsTQYgDlOecW5muS2Ey_GV&wd=&eqid=939721830002c7ff000000025ad5e89c'
    }
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        print('请求失败！')
        return None

def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    # 电影名
    name = []
    items = soup.find_all('div', class_='hd')
    for item in items:
        name.append(item.a.span.text)
    # 评分
    rank = []
    items = soup.find_all('div', class_='star')
    for item in items:
        rank.append(item.span.next_sibling.next_sibling.text) # 请区别next_sibling和next_sibling的区别，以及previous.....
    #资料
    message = []
    items = soup.find_all('div', class_='star')
    for item in items:
        item = item.previous_sibling.previous_sibling.text.split('\n') # 这里使用了两个previous_sibling,注意块级元素一般会有个空行
        try:
            message.append(item[1].strip() + item[2].strip())
        except:
            continue
    data = []
    length = len(name)
    for each in range(length):
        data.append([name[each], rank[each], message[each]])
    return data

def find_depth(html):
    soup = BeautifulSoup(html, 'lxml')
    depth = soup.find('span', class_='next').previous_sibling.previous_sibling.text # 注意两个previous_sibling
    return int(depth)

def save_to_excel(data):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['电影', '排名', '资料'])
    for each in data:
        ws.append(each)
    wb.save('doubantop250.xlsx')

def main():
    url = 'https://movie.douban.com/top250'
    html = get_one_page(url)
    depth = find_depth(html)
    results = []
    for each in range(depth):
        page_url = url + '?start=' + str(25*each)
        html = get_one_page(page_url)
        results.extend(parse_one_page(html))
    save_to_excel(results)

if __name__ == '__main__':
    main()

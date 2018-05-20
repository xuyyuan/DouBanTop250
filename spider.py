import requests
import bs4
import re

def open_url(url):
	#使用代理
	# proxies = {'http':'127.0.0.1:1080':'https':'127.0.0.1:1080'}#注意proxies和headers是字典
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
	# res = requests.get(url, headers=headers, proxies=proxies)
	res = requests.get(url, headers=headers)
	return res

def find_depth(res):
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	depth = soup.find('span', class_="next").previous_sibling.previous_sibling.text
	# .previous_sibling.previous_sibling.text
	# print(depth)
	return int(depth)

def find_movies(res): # 找一页的内容
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	#电影名
	movies = []
	targets = soup.find_all('div', class_="hd")
	for each in targets:
		movies.append(each.a.span.text)
	#评分
	ranks = []
	targets = soup.find_all('span', class_="rating_num")
	for each in targets:
		ranks.append('评分是：%s' % each.text)
	#资料
	messages = []
	targets = soup.find_all('div', class_="bd")
	for each in targets:
		each_split = each.p.text.split('\n')
		try: # 这里最好打上一个try语句
			#messages.append(each.p.text.split('\n')[1].strip() + each.p.text.split('\n')[2].strip())
			messages.append(each_split[1].strip() + each_split[2].strip())#没搞清楚索引和strip()
			# split分割的时候要注意html文件中的内容 有没有空格！！
		except:
			continue	
	result = []  # 函数内的变量只能在函数内使用哦，与下面的result不同哦！
	length = len(movies) # 注意len()函数
	for i in range(length): 
		result.append(movies[i] + ranks[i] + messages[i] + '\n') # 注意最好加‘\n’ 换行
	return result # 缩进的问题要注意

def main():
	host = 'https://movie.douban.com/top250?' # 后面有个问号，最好先在这里加上，弄忘了可不好
	res = open_url(host)
	depth = find_depth(res)
	result = []
	for i in range(depth):
		url = host + 'start=' + str(25*i)
		res = open_url(url)
		result.extend(find_movies(res)) # 注意是extend() 添加多个列表元素，里面的参数应该是列表，注意append和extend的区别
	with open('doubantop250.txt', 'w', encoding='utf-8') as f: # 注意编码的问题gbk编码
		for each in result:
			f.write(each)

if __name__ == '__main__':
	main()




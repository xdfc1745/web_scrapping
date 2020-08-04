import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://movie.naver.com/movie/running/current.nhn'

response = requests.get(URL)
# print(response.text)
soup = BeautifulSoup(response.text, 'html.parser')

li = soup.select('div[class=lst_wrap] > ul[class=lst_detail_t1] > li')

for a in li:
    href = a.select_one('dt[class=tit] > a')['href']
    title = a.select_one('dt[class=tit] > a').getText()
    code = href.split('=')
    movie = {
        'title': title,
        'code': code[1]
    }
    print(movie)

# print(code)

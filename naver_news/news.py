import requests
from bs4 import BeautifulSoup
import csv

f = open('news.csv', 'w', newline='', encoding='utf-8-sig')
wr = csv.writer(f)
wr.writerow(['title', 'href'])

soup_objects = []

for i in range(1, 102, 10):
    base_url = 'https://search.naver.com/search.naver?&where=news&query=%EA%B4%91%EC%A3%BC%20%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%20%EC%82%AC%EA%B4%80%ED%95%99%EA%B5%90&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=32&start='
    start_num = i
    end_url = '&refresh_start=0'

    URL = base_url + str(start_num) + end_url

    response = requests.get(URL)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup_objects.append(soup)

    for soup in soup_objects:
        # find, find_all보다 select_one, select가 더 빠르고 효율적이다
        news_section = soup.select(
            'div[id=wrap] > div[id=container] > div[id=content] > div[id=main_pack] > div.news.mynews.section._prs_nws > ul > li')
        # print(news_section)

        # a태그 안에 title, href를 가져오기(구글링)
        for news in news_section:
            href = news.select_one('dl > dt > a')['href']
            title = news.select_one('dl > dt > a')['title']
            # print(title)
            # print(href, '\n')

            wr.writerow([title, href])

f.close()

import requests
from bs4 import BeautifulSoup


URL = 'https://movie.naver.com/movie/running/current.nhn'

response = requests.get(URL)
# print(response.text)
soup = BeautifulSoup(response.text, 'html.parser')

li = soup.select('div[class=lst_wrap] > ul[class=lst_detail_t1] > li')

movie_data = []
for a in li:
    href = a.select_one('dt[class=tit] > a')['href']
    title = a.select_one('dt[class=tit] > a').getText()
    code = href.split('=')
    # href.find('code=' + len('code='))
    movie = {
        'title': title,
        'code': code[1]
    }
    # print(movie)
    movie_data.append(movie)

headers = {
    'authority': 'movie.naver.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=189069',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=OBIMYEXGXMVV6; BMR=s=1596701694852&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.nhn%3FblogId%3Dsskids0912%26logNo%3D221469950078%26proxyReferer%3Dhttps%3A%252F%252Fwww.google.com%252F&r2=https%3A%2F%2Fwww.google.com%2F; NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; csrf_token=35b5b0b7-9c8a-4bc9-98d0-841078c06585',
}


for movie in movie_data:
    code = movie['code']

    params = (
        ('code', code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )
    URL = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code={code}'
    re_response = requests.get(URL, headers=headers, params=params)
    re_soup = BeautifulSoup(re_response.text, 'html.parser')

    ul = re_soup.select('div[class=score_result] > ul > li')

    idx = 0
    for i, li in enumerate(ul):
        score = li.select_one('div[class=star_score] > em').getText()  # 평점
        # 리뷰의 길이가 짧은 경우
        if li.select_one(f'div.score_reple > p > span[id=_filtered_ment_{i}] > span#_unfold_ment{i}') is None:
            review = li.select_one(
                f'div.score_reple > p > span[id=_filtered_ment_{i}]')
        else:  # 리뷰의 길이가 길어서 페이지를 이동해야하는 경우
            review = li.select_one(
                f'div.score_reple > p > span[id=_filtered_ment_{i}]').getText().strip()

        print(score, " ", review, " ", )
        idx += 1

import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://movie.naver.com/movie"

def get_page(page_url): # URL을 받아 페이지를 가져와서 파싱한 두 결과를 리턴
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup, page


def get_avg_stars(reviews): # 리뷰 리스트를 받아 평균 별점을 구해 리턴
    star = []
    for i in reviews:
        star += [i['review_star']]
    avg = sum(star) / len(star)

    return avg


def get_movie_code(movie_title): # 영화 제목을 검색해 코드 추출
    search_url = f"{BASE_URL}/search/result.naver?query={movie_title}&section=all&ie=utf8"
    soup = get_page(search_url)[0]
    movie_code = int(soup.find(class_='result_thumb').find('a')['href'].split('=')[1]) # 'reult_thumb' class에서 href를 가져와 '='로 split한 뒤 추출

    return movie_code


def get_reviews(movie_code, page_num=1):
    review_url = f"{BASE_URL}/point/af/list.naver?st=mcode&sword={movie_code}&target=after&page={page_num}"
    review_list = []
    soup = get_page(review_url)[0] # 위에서 만든 Get page 함수 중 suop만 가져오기
    for i in soup.find_all(class_='title'): # 'title' class를 모두 가져와 for문으로 추출
        review_list.append({
            'review_text': i.text.split('\n')[5], # text화 시켜 '\n'을 기준으로 split한 후 선택
            'review_star': int(i.find('em').text) # em을 가져와 text만 추출 후 int화
        })
    return review_list


def scrape_by_review_num(movie_title, review_num): # 영화 이름과 총 스크래핑할 리뷰 수를 받아 해당 수만큼 항목이 담긴 리스트 리턴
    reviews = []
    page_num = 1
    while len(reviews) < review_num:
        reviews += get_reviews(get_movie_code(movie_title), page_num)
        page_num += 1
    return reviews[:review_num]


def scrape_by_page_num(movie_title, page_num=10): # 영화 이름과 총 스크래핑할 페이지 수를 받아 해당 페이지만큼 항목이 담긴 리스트 리턴
    reviews = []
    for i in range(page_num):
        reviews += get_reviews(get_movie_code(movie_title), i)
    return reviews
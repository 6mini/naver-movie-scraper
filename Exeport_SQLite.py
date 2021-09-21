import os
import sqlite3
from . import Web_Scraping

DATABASE_PATH = os.path.join(os.getcwd(), 'scrape_data.db')
conn = sqlite3.connect(DATABASE_PATH)

def store_by_page_num(movie_title, page_num=10, conn=conn): # 영화제목, 페이지 수를 받아 스크래핑한 뒤 DB에 저장
    cur = conn.cursor()
    Review = Web_Scraping.scrape_by_page_num(movie_title, page_num)
    id = 0
    for row in Review:
        cur.execute(
        "INSERT INTO Review (id, review_text, review_star, movie_title) VALUES (?, ?, ?, ?)",
        (id, row['review_text'], row['review_star'], movie_title)
        )
        id += 1
    conn.commit()

def init_db(conn=conn): # Review 테이블 초기화 함수
    create_table = """CREATE TABLE Review (
                        id INTEGER,
                        review_text TEXT,
                        review_star FLOAT,
                        movie_title VARCHAR(128),
                        PRIMARY KEY (id)
                        );"""

    drop_table_if_exists = "DROP TABLE IF EXISTS Review;"

    cur = conn.cursor()

    cur.execute(drop_table_if_exists)
    cur.execute(create_table)
    cur.close()

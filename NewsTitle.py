from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

# 뉴스 검색 날짜 지정
NEWS_URL = ['https://news.naver.com/breakingnews/section/105/230?date={}',
            'https://news.naver.com/breakingnews/section/105/229?date={}'] # IT과학

# 카테고리 이름 
category = ['IT일반',
            '게임/리뷰']

DATE = ['20250416', '20250415']

#최종 입력 제목, 내용, 링크
link = []
title = []
content = []

#날짜
for m_date in DATE :
        
        category_idx = 0
        #카테고리별
        for news_url in NEWS_URL :

                #날짜 카테고리 입력
                title.append(category[category_idx] + ' ' + m_date)
                content.append(' ')
                link.append(' ')

                #링크접속
                complit_url = news_url.format(m_date)

                driver.get(complit_url)
                time.sleep(3)

                # 더보기 버튼 찾기 및 오류 시 한번만 재시도
                try:
                        search_box = driver.find_element(By.XPATH, '//*[@id="newsct"]/div[2]/div/div[2]/a')
                except Exception as e:
                        driver.get(complit_url)
                        time.sleep(3)
                        search_box = driver.find_element(By.XPATH, '//*[@id="newsct"]/div[2]/div/div[2]/a')

                # 버튼 누루기기
                for i in range(1,1000):
                        try:
                                search_box.click()
                        except Exception as e:
                                break
                

                selenium_html = driver.page_source

                # BeautifulSoup으로 전부 로딩된 페이지 html 받아오기
                soup = BeautifulSoup(selenium_html, 'html.parser')

                blocks = soup.select('.sa_text')

                for block in blocks:
                        text_all = block.text
                        text_all = text_all.strip()
                        # text_arr[0] 제목, text_arr[2] 일부 내용
                        text_arr = text_all.split('\n')

                        #링크
                        m_link = block.contents[1].attrs['href']

                        name_search = True
                        
                        link.append(m_link)
                        title.append(text_arr[0])
                        content.append(text_arr[2])

                category_idx += 1

count = 0

data_list = { '기사 제목':title, '내용':content, '링크':link}

df = pd.DataFrame(data_list)

df.drop_duplicates(subset='기사 제목')

df.to_csv('뉴스기사.csv', index=False, encoding='utf-8-sig')

print('작업 완료')

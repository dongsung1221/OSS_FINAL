print("")

import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import tkinter as tk

# URL 설정
url = "https://en.yna.co.kr/news"

# 페이지 요청
response = requests.get(url)

# HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# <strong class="tit"> 태그 내에서 모든 기사 제목 찾기
articles = soup.find_all('strong', class_='tit')

# 3번째 기사 제목과 URL 출력 (인덱스는 2부터 시작)
if len(articles) >= 3:
    third_article = articles[2]
    article_title = third_article.get_text(strip=True)
    article_url = third_article.find('a')['href']
    
    # 절대 URL로 변환
    if article_url.startswith('https://'):
        print(f"기사 제목: {article_title}")
        print(f"URL: {article_url}")
    else:
        print(f"기사 제목: {article_title}")
        print(f"URL: https://en.yna.co.kr{article_url}")
else:
    print("3번째 기사를 찾을 수 없습니다.")

print("")
url = "https://en.yna.co.kr/view/AEN20241217008100320"

# 페이지 요청
response = requests.get(article_url)

# HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# <article> 태그 안의 본문을 찾기
article = soup.find('article', class_='story-news')

# 본문 텍스트만 추출
if article:
    paragraphs = article.find_all('p')
    text = ""  # 텍스트를 이어붙이기 위해 초기화
    for p in paragraphs:
        text += p.get_text() + " "  # 각 문단을 이어붙임

# 이어붙인 전체 본문 확인
print("전체 기사 본문:")
print(text)

print("")

# 요약 모델 설정
summarizer = pipeline("summarization")

# 텍스트 요약하기
if text:  # text가 비어있지 않을 때만 요약 수행
    summary = summarizer(text, max_length=500, min_length=30, do_sample=False)
    print("요약된 내용:")
    print(summary[0]['summary_text'])
else:
    print("요약할 본문이 없습니다.")



# 첫 번째 창 생성
root1 = tk.Tk()
root1.title("원본기사")
root1.geometry("400x800")  # 창 크기 설정

# 첫 번째 창에 텍스트 레이블 추가
label1 = tk.Label(root1, text=text, font=("Arial", 12), wraplength=380)
label1.pack(pady=40)

# 두 번째 창 생성
root2 = tk.Toplevel()  # 새 창 생성
root2.title("기사 요약")
root2.geometry("400x500")  # 창 크기 설정

# 두 번째 창에 텍스트 레이블 추가
label2 = tk.Label(root2, text=summary, font=("Arial", 12), wraplength=380)
label2.pack(pady=40)

# 두 개의 창이 모두 띄워지도록 메인 루프 실행
root1.mainloop()

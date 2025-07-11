import os
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

import matplotlib
matplotlib.rcParams['font.family'] = 'Malgun Gothic'  # Windows 기준
matplotlib.rcParams['axes.unicode_minus'] = False     # 마이너스 깨짐 방지


from django.shortcuts import render
from django.conf import settings


def index(request):
    weather = None
    location = request.GET.get('location')

    if location:
        # 네이버 날씨 검색 페이지
        url = f"https://search.naver.com/search.naver?query={location}+날씨"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        try:
            # 크롤링 대상 클래스는 페이지 구조 따라 달라질 수 있음!
            temp = soup.select_one(".temperature_text").text.strip()
            desc = soup.select_one(".summary").text.strip()
            weather = f"{temp} / {desc}"

            # 샘플 그래프 데이터 (시간별 온도)
            hours = ['6시', '9시', '12시', '15시', '18시']
            temps = [20, 22, 25, 24, 21]

            # 그래프 이미지 저장 경로
            graph_path = os.path.join(settings.BASE_DIR, 'weatherapp', 'static', 'graph.png')
            os.makedirs(os.path.dirname(graph_path), exist_ok=True)

            # 그래프 그리기
            plt.figure(figsize=(6, 4))
            plt.plot(hours, temps, marker='o')
            plt.title(f"{location} 기온 변화 예측")
            plt.xlabel("시간대")
            plt.ylabel("기온 (℃)")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(graph_path)
            plt.close()

        except Exception as e:
            weather = "날씨 정보를 불러올 수 없습니다."

    return render(request, 'index.html', {
        'weather': weather,
        'location': location
    })

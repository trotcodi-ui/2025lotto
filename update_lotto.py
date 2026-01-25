import requests
from bs4 import BeautifulSoup
import json
import os

# 파일 경로 및 결과 페이지 URL
LOTTO_JSON_PATH = '2025lotto_numbers_1_to_1182_final.json'
BASE_URL = "https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo="

def update_lotto_data():
    # 1. 기존 데이터 로드
    if os.path.exists(LOTTO_JSON_PATH):
        try:
            with open(LOTTO_JSON_PATH, 'r', encoding='utf-8') as f:
                lotto_data = json.load(f)
        except:
            lotto_data = []
    else:
        lotto_data = []

    last_draw = max([d['draw_no'] for d in lotto_data]) if lotto_data else 0
    target_draw = last_draw + 1
    print(f"조회 시도 회차: {target_draw}회")

    # 2. 브라우저처럼 보이기 위한 헤더 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Referer": "https://www.dhlottery.co.kr/"
    }

    try:
        # 페이지 소스 가져오기
        response = requests.get(f"{BASE_URL}{target_draw}", headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. HTML에서 당첨 번호 추출 (클래스명 기반)
        # 동행복권 페이지의 당첨번호 공(ball_64) 클래스를 찾습니다.
        win_balls = soup.select('.num.win .ball_64')
        bonus_ball = soup.select_one('.num.bonus .ball_64')
        date_text = soup.select_one('.desc') # 추첨 날짜

        if win_balls and bonus_ball:
            numbers = [int(ball.text) for ball in win_balls]
            bonus = int(bonus_ball.text)
            draw_date = date_text.text.strip().replace('(', '').replace(')익일 추첨', '')

            new_entry = {
                "draw_no": target_draw,
                "date": draw_date,
                "numbers": numbers,
                "bonus": bonus
            }

            lotto_data.append(new_entry)
            lotto_data.sort(key=lambda x: x['draw_no'], reverse=True)

            with open(LOTTO_JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump(lotto_data, f, ensure_ascii=False, indent=4)
            print(f"✅ {target_draw}회 데이터 수동 추출 성공!")
        else:
            print(f"❌ {target_draw}회 데이터를 페이지에서 찾을 수 없습니다. (아직 업데이트 전일 수 있음)")

    except Exception as e:
        print(f"❗ 오류 발생: {e}")

if __name__ == "__main__":
    update_lotto_data()

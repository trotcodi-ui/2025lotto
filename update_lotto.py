import requests
from bs4 import BeautifulSoup
import json
import os

# 파일 경로 및 결과 페이지 URL
LOTTO_JSON_PATH = '2025lotto_numbers_1_to_1182_final.json'
BASE_URL = "https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo="

def update_lotto_data():
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

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(f"{BASE_URL}{target_draw}", headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. 당첨 번호 찾기 (id 기반으로 더 정확하게 접근)
        win_balls = soup.find_all('span', class_='ball_64')
        
        # 날짜 찾기 (desc 클래스 안의 텍스트)
        date_tag = soup.select_one('.desc')
        draw_date = date_tag.text.strip().split('(')[0].strip() if date_tag else ""

        if len(win_balls) >= 7:
            # 앞의 6개는 당첨번호, 마지막 1개는 보너스번호
            numbers = [int(ball.text) for ball in win_balls[:6]]
            bonus = int(win_balls[6].text)

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
            print(f"❌ {target_draw}회 번호를 찾지 못했습니다. (추첨 전이거나 태그 불일치)")

    except Exception as e:
        print(f"❗ 오류 발생: {e}")

if __name__ == "__main__":
    update_lotto_data()

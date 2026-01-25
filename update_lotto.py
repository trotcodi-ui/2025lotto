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

        # 해당 회차 데이터가 페이지에 있는지 확인 (회차 선택 박스 확인)
        selected_option = soup.select_one('#dwrNoList option[selected]')
        actual_draw = int(selected_option.text) if selected_option else 0

        if actual_draw == target_draw:
            # 당첨 번호 6개와 보너스 번호 추출
            win_balls = soup.select('.num.win .ball_64')
            bonus_ball = soup.select_one('.num.bonus .ball_64')
            date_tag = soup.select_one('.desc')
            
            if win_balls and bonus_ball:
                numbers = [int(ball.text) for ball in win_balls]
                bonus = int(bonus_ball.text)
                draw_date = date_tag.text.strip().split('(')[0].strip() if date_tag else ""

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
                print(f"❌ 번호 태그를 찾을 수 없습니다.")
        else:
            print(f"❌ 아직 {target_draw}회차 결과가 홈페이지에 업데이트되지 않았습니다.")

    except Exception as e:
        print(f"❗ 오류 발생: {e}")

if __name__ == "__main__":
    update_lotto_data()

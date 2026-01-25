import requests
from bs4 import BeautifulSoup
import json
import os

LOTTO_JSON_PATH = '2025lotto_numbers_1_to_1182_final.json'

def get_lotto_via_scraping(draw_no):
    # 동행복권 메인 결과 페이지 (Gemini가 주로 확인하는 경로)
    url = f"https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo={draw_no}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. 회차 확인 (사용자가 요청한 회차가 맞는지 검증)
        target_check = soup.select_one('h4 strong')
        if not target_check or str(draw_no) not in target_check.text:
            return None

        # 2. 번호 추출
        balls = soup.select('.num.win .ball_64')
        bonus = soup.select_one('.num.bonus .ball_64')
        date_tag = soup.select_one('.desc')

        if len(balls) == 6 and bonus:
            return {
                "draw_no": draw_no,
                "date": date_tag.text.split('(')[0].strip() if date_tag else "",
                "numbers": [int(b.text) for b in balls],
                "bonus": int(bonus.text)
            }
    except:
        return None
    return None

def update_lotto_data():
    if os.path.exists(LOTTO_JSON_PATH):
        with open(LOTTO_JSON_PATH, 'r', encoding='utf-8') as f:
            lotto_data = json.load(f)
    else:
        lotto_data = []

    last_draw = max([d['draw_no'] for d in lotto_data]) if lotto_data else 0
    target_draw = last_draw + 1
    print(f"🎯 Gemini 방식 추적 시작 - 목표: {target_draw}회")

    # 데이터 가져오기 시도
    result = get_lotto_via_scraping(target_draw)

    if result:
        lotto_data.append(result)
        lotto_data.sort(key=lambda x: x['draw_no'], reverse=True)
        with open(LOTTO_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(lotto_data, f, ensure_ascii=False, indent=4)
        print(f"✅ {target_draw}회 업데이트 성공! (Gemini 방식 적용)")
    else:
        print(f"❌ {target_draw}회차는 아직 공식 홈페이지에 반영되지 않았거나 차단되었습니다.")

if __name__ == "__main__":
    update_lotto_data()

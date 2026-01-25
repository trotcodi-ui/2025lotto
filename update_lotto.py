import requests
from bs4 import BeautifulSoup
import json
import os

LOTTO_JSON_PATH = '2025lotto_numbers_1_to_1182_final.json'

def get_lotto_from_portal(draw_no):
    # 포털의 로또 검색 결과 페이지 흉내 (검색 결과로 바로 접근)
    url = f"https://search.naver.com/search.naver?query={draw_no}회+로또"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 네이버 검색 결과 내 당첨 번호 추출 (구조는 주기적으로 변하지만 현재 가장 확실한 방법)
        balls = soup.select('.num_box .num')
        date_tag = soup.select_one('.sub_title')

        if len(balls) >= 7:
            numbers = [int(b.text) for b in balls[:6]]
            bonus = int(balls[6].text)
            
            return {
                "draw_no": draw_no,
                "date": date_tag.text if date_tag else "2026-01-24", # 예시 날짜
                "numbers": numbers,
                "bonus": bonus
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
    
    print(f"🔎 Gemini 방식(포털 추적) 가동 - 목표: {target_draw}회")

    result = get_lotto_from_portal(target_draw)

    if result:
        lotto_data.append(result)
        lotto_data.sort(key=lambda x: x['draw_no'], reverse=True)
        with open(LOTTO_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(lotto_data, f, ensure_ascii=False, indent=4)
        print(f"✅ {target_draw}회 업데이트 완료! (포털 우회 성공)")
    else:
        print(f"❌ 아직 포털에도 {target_draw}회 결과가 올라오지 않았거나 차단되었습니다.")

if __name__ == "__main__":
    update_lotto_data()

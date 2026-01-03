import json
import os
import requests
import re

file_path = "2025lotto_numbers_1_to_1182_final.json"

# 기존 데이터 불러오기
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

last_draw = data[0]["draw_no"] if data else 0
next_draw = last_draw + 1
print(f"🔍 현재 마지막 회차: {last_draw}, 다음 시도 회차: {next_draw}")

# 네이버 로또 검색 결과 주소 (우회용)
url = f"https://search.naver.com/search.naver?query={next_draw}회로또"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

try:
    res = requests.get(url, headers=headers, timeout=15)
    html = res.text

    # 네이버 검색 결과에서 당첨번호 패턴 추출
    numbers = re.findall(r'<span class="ball_n.*?">(\d+)</span>', html)
    
    if len(numbers) >= 7:
        win_numbers = [int(n) for n in numbers[:6]]
        bonus = int(numbers[6])
        
        new_entry = {
            "draw_no": next_draw,
            "numbers": win_numbers,
            "bonus": bonus
        }
        data.insert(0, new_entry)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 네이버를 통해 {next_draw}회차 업데이트 완료: {win_numbers} + {bonus}")
    else:
        print("🚫 데이터를 찾을 수 없습니다. 아직 업데이트 전이거나 네이버도 접속을 제한했습니다.")
        exit(1) # 에러로 표시하여 인지할 수 있게 함

except Exception as e:
    print(f"❌ 오류 발생: {e}")
    exit(1)

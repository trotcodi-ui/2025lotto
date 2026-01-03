import json
import os
import requests

file_path = "2025lotto_numbers_1_to_1182_final.json"

# 1. 파일 읽기
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

last_draw = data[0]["draw_no"] if data else 0
next_draw = last_draw + 1

print(f"🔍 현재 마지막 회차: {last_draw}, 시도 회차: {next_draw}")

# 2. API 호출 (사람인 것처럼 헤더 추가)
headers = {'User-Agent': 'Mozilla/5.0'}
url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={next_draw}"

res = requests.get(url, headers=headers)
info = res.json()

# 3. 데이터 확인 및 저장
if info.get("returnValue") == "success":
    numbers = [info[f"drwtNo{i}"] for i in range(1, 7)]
    bonus = info["bnusNo"]
    new_entry = {"draw_no": next_draw, "numbers": numbers, "bonus": bonus}
    
    data.insert(0, new_entry)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ {next_draw}회차 저장 완료: {numbers}")
else:
    print(f"🚫 API에서 데이터를 가져오지 못했습니다. 응답값: {info}")
    # 데이터가 없으면 액션을 실패로 표시하여 사용자에게 알림
    exit(1)

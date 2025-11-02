import json
import os
import requests

# JSON 파일 경로
file_path = "2025lotto_numbers_1_to_1182_final.json"

# 기존 데이터 불러오기
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

# 최신 회차 구하기 (내림차순 구조니까 data[0]이 최신)
last_draw = data[0]["draw_no"] if data else 0
next_draw = last_draw + 1

print(f"🔍 현재 마지막 회차: {last_draw}, 다음 시도 회차: {next_draw}")

# 동행복권 API 호출
url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={next_draw}"

res = requests.get(url)
info = res.json()

if info.get("returnValue") != "success":
    print(f"🚫 {next_draw}회차는 아직 발표되지 않음. 종료합니다.")
else:
    numbers = [info[f"drwtNo{i}"] for i in range(1, 7)]
    bonus = info["bnusNo"]
    new_entry = {
        "draw_no": next_draw,
        "numbers": numbers,
        "bonus": bonus
    }
    # 내림차순 구조 유지 → 앞에 삽입
    data.insert(0, new_entry)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ {next_draw}회차 추가 완료: {numbers} + 보너스 {bonus}")

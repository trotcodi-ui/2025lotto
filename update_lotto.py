import json
import requests
import os

# JSON 파일 경로
file_path = "2025lotto_numbers_1_to_1182_final.json"

# 기존 데이터 불러오기
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

# 가장 최근 회차 번호 구하기
last_draw = data[-1]["draw_no"] if data else 1182
next_draw = last_draw + 1

print(f"🌀 최신 회차 번호 확인 중... ({next_draw}회)")

# 동행복권 API (네이버보다 안정적)
url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={next_draw}"
res = requests.get(url)
info = res.json()

# 데이터 유효성 확인
if info.get("returnValue") == "success":
    numbers = [info[f"drwtNo{i}"] for i in range(1, 7)]
    bonus = info["bnusNo"]
    data.append({
        "draw_no": next_draw,
        "numbers": numbers,
        "bonus": bonus
    })

    # JSON 덮어쓰기
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ {next_draw}회차 로또 번호 업데이트 완료: {numbers} + 보너스 {bonus}")
else:
    print(f"⚠️ {next_draw}회차 데이터가 아직 공개되지 않았습니다.")

import json
import requests
import os
import time

# JSON 파일 경로
file_path = "2025lotto_numbers_1_to_1182_final.json"

# 기존 데이터 불러오기
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

# 가장 마지막 회차 번호 구하기
last_draw = data[-1]["draw_no"] if data else 1182
next_draw = last_draw + 1

print(f"🌀 현재 JSON의 마지막 회차: {last_draw} → 다음 가져올 회차: {next_draw}")

# 동행복권 공식 API
API_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="

# 새로운 회차 자동으로 모두 가져오기
while True:
    url = f"{API_URL}{next_draw}"
    res = requests.get(url)
    info = res.json()

    if info.get("returnValue") != "success":
        print(f"⚠️ {next_draw}회차 데이터가 아직 없습니다. 업데이트 완료.")
        break

    numbers = [info[f"drwtNo{i}"] for i in range(1, 7)]
    bonus = info["bnusNo"]

    data.append({
        "draw_no": next_draw,
        "numbers": numbers,
        "bonus": bonus,
        "date": info["drwNoDate"]
    })

    print(f"✅ {next_draw}회차 추가 완료: {numbers} + 보너스 {bonus}")
    next_draw += 1
    time.sleep(0.5)  # API 서버 과부하 방지용

# 파일 저장
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("🎉 모든 누락 회차 자동 업데이트 완료!")

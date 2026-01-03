import json
import os
import requests
import time

# =========================
# 설정
# =========================
FILE_PATH = "2025lotto_numbers_1_to_1182_final.json"
BASE_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.dhlottery.co.kr/"
}

# =========================
# 기존 데이터 로드
# =========================
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

# 최신 회차 (내림차순 구조)
last_draw = data[0]["draw_no"] if data else 0
next_draw = last_draw + 1

print(f"🔍 마지막 저장 회차: {last_draw}")
print(f"➡️  시도 회차: {next_draw}")

# =========================
# API 호출 (재시도 포함)
# =========================
info = None

for attempt in range(3):
    try:
        res = requests.get(
            BASE_URL.format(next_draw),
            headers=HEADERS,
            timeout=10
        )
        info = res.json()

        if info.get("returnValue") == "success":
            break
        else:
            print(f"⏳ {next_draw}회차 아직 미발표 (시도 {attempt + 1}/3)")
    except Exception as e:
        print(f"⚠️ 요청 실패 (시도 {attempt + 1}/3): {e}")

    time.sleep(2)

# =========================
# 결과 처리
# =========================
if not info or info.get("returnValue") != "success":
    print(f"🚫 {next_draw}회차 데이터 없음. 종료.")
    exit(0)

numbers = [info[f"drwtNo{i}"] for i in range(1, 7)]
bonus = info["bnusNo"]

new_entry = {
    "draw_no": next_draw,
    "numbers": numbers,
    "bonus": bonus
}

# 내림차순 유지 → 맨 앞에 삽입
data.insert(0, new_entry)

# =========================
# 파일 저장
# =========================
with open(FILE_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ {next_draw}회차 업데이트 완료")
print(f"🎯 번호: {numbers} + 보너스 {bonus}")

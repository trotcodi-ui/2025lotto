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
# 데이터 로드
# =========================
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

# 이미 저장된 회차 집합 (중복 방지)
existing_draws = {d["draw_no"] for d in data}

# 최신 회차 계산 (안전)
last_draw = max(existing_draws) if existing_draws else 0
next_draw = last_draw + 1

print(f"🔍 현재 최신 회차: {last_draw}")
print(f"➡️ 다음 시도 회차: {next_draw}")

# =========================
# 자동 복구 / 업데이트 루프
# =========================
added = 0

while True:
    try:
        res = requests.get(
            BASE_URL.format(next_draw),
            headers=HEADERS,
            timeout=10
        )
        info = res.json()
    except Exception as e:
        print(f"⚠️ 요청 오류: {e}")
        break

    # API 미오픈 → 중단
    if info.get("returnValue") != "success":
        print(f"⏹ {next_draw}회차 API 미오픈. 종료")
        break

    # 혹시 모를 중복 방지
    if next_draw in existing_draws:
        print(f"⚠️ {next_draw}회차 이미 존재 → 스킵")
        next_draw += 1
        continue

    numbers = [info[f"drwtNo{i}"] for i in range(1, 7)]
    bonus = info["bnusNo"]

    data.insert(0, {
        "draw_no": next_draw,
        "numbers": numbers,
        "bonus": bonus
    })

    existing_draws.add(next_draw)
    added += 1

    print(f"✅ {next_draw}회차 추가 완료 → {numbers} + 보너스 {bonus}")

    next_draw += 1
    time.sleep(1)

# =========================
# 저장
# =========================
if added > 0:
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"🎉 총 {added}개 회차 업데이트 완료")
else:
    print("ℹ️ 추가된 회차 없음 (이미 최신)")

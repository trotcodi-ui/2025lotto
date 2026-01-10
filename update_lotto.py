import json
import os
import requests
import time

# =========================
# 설정: 파일 경로 및 API 주소
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
# 데이터 로드 (기존 파일 읽기)
# =========================
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

# 이미 저장된 회차 집합 (중복 방지용)
existing_draws = {d["draw_no"] for d in data}

# 최신 회차 계산 (가장 큰 번호 찾기)
last_draw = max(existing_draws) if existing_draws else 0
next_draw = last_draw + 1

print(f"🔍 현재 파일 내 최신 회차: {last_draw}")
print(f"➡️ 업데이트 시작 회차: {next_draw}")

# =========================
# 자동 업데이트 루프 (원본 로직 유지)
# =========================
added = 0

while True:
    try:
        res = requests.get(
            BASE_URL.format(next_draw),
            headers=HEADERS,
            timeout=10
        )
        # API 응답 체크
        if res.status_code != 200:
            print(f"⚠️ 연결 오류 (HTTP {res.status_code}). 중단합니다.")
            break
            
        info = res.json()
    except Exception as e:
        print(f"⚠️ 요청 오류: {e}")
        break

    # API 미오픈(아직 추첨 전) 시 종료
    if info.get("returnValue") != "success":
        print(f"⏹ {next_draw}회차 API 미오픈. 업데이트를 완료합니다.")
        break

    # 중복 방지 체크
    if next_draw in existing_draws:
        print(f"⚠️ {next_draw}회차 이미 존재 → 스킵")
        next_draw += 1
        continue

    # 당첨 번호 및 보너스 번호 파싱
    numbers = [info[f"drwtNo{i}"] for i in range(1, 7)]
    bonus = info["bnusNo"]

    # 데이터의 맨 앞(0번 인덱스)에 삽입 (최신순 유지)
    data.insert(0, {
        "draw_no": next_draw,
        "numbers": numbers,
        "bonus": bonus
    })

    print(f"✅ {next_draw}회차 추가 완료 → {numbers} + 보너스 {bonus}")

    existing_draws.add(next_draw)
    added += 1
    next_draw += 1
    time.sleep(1) # 서버 부하 방지 (1초 대기)

# =========================
# 파일 저장 (변경된 내용이 있을 때만)
# =========================
if added > 0:
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        # ensure_ascii=False로 한글 깨짐 방지, indent=2로 가독성 확보
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"🎉 총 {added}개 회차 업데이트 완료 및 {FILE_PATH} 저장 성공!")
else:
    print("ℹ️ 추가된 회차 없음 (이미 모든 데이터가 최신입니다)")

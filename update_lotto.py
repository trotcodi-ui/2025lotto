import json
import os
import requests
import time

# =========================
# 설정: 파일 경로 및 API 주소
# =========================
# 💡 현재 파이썬 파일이 있는 위치를 기준으로 JSON 파일을 찾습니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "2025lotto_numbers_1_to_1182_final.json")
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
    print(f"📂 기존 파일을 불러왔습니다: {FILE_PATH}")
else:
    # 만약 파일 이름이 틀렸다면 여기서 새로 빈 파일을 만들게 됩니다.
    # 리포지토리의 파일명과 대소문자까지 똑같은지 꼭 확인하세요!
    print(f"⚠️ 파일을 찾을 수 없어 새로 생성합니다: {FILE_PATH}")
    data = []

# 이미 저장된 회차 추출
existing_draws = {d["draw_no"] for d in data}
last_draw = max(existing_draws) if existing_draws else 0
next_draw = last_draw + 1

print(f"🔍 현재 최신 회차: {last_draw} -> 다음 목표: {next_draw}")

# =========================
# 업데이트 루프
# =========================
added = 0
while True:
    try:
        res = requests.get(BASE_URL.format(next_draw), headers=HEADERS, timeout=10)
        info = res.json()
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        break

    if info.get("returnValue") != "success":
        print(f"⏹ {next_draw}회차 데이터가 아직 없습니다. (종료)")
        break

    # 데이터 추가
    numbers = [info[f"drwtNo{i}"] for i in range(1, 7)]
    bonus = info["bnusNo"]
    
    data.append({
        "draw_no": next_draw,
        "numbers": numbers,
        "bonus": bonus
    })
    
    print(f"✅ {next_draw}회차 추가 성공!")
    added += 1
    next_draw += 1
    time.sleep(1)

# =========================
# 정렬 및 저장
# =========================
if added > 0:
    # 최신 회차가 맨 위로 오도록 내림차순 정렬
    data.sort(key=lambda x: x["draw_no"], reverse=True)
    
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"🎉 총 {added}개 회차 업데이트 완료!")
else:
    print("ℹ️ 추가할 새로운 회차가 없습니다.")

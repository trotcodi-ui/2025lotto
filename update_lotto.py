import json
import os
import requests
import time

# JSON 파일 경로
file_path = "2025lotto_numbers_1_to_1182_final.json"

# 기존 데이터 불러오기
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

# 현재 최신 회차 확인
last_draw = data[-1]["draw_no"] if data else 0
next_draw = last_draw + 1
print(f"📢 현재 최신 회차: {last_draw} → 다음 회차: {next_draw}")

# 동행복권 API 기본 URL
API_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="

def fetch_draw(draw_no):
    """특정 회차 로또번호 가져오기 (최대 5회 재시도)"""
    url = API_URL + str(draw_no)
    for attempt in range(5):
        try:
            res = requests.get(url, timeout=5)
            info = res.json()
            if info.get("returnValue") == "success":
                numbers = [info[f"drwtNo{i}"] for i in range(1, 7)]
                bonus = info["bnusNo"]
                return {
                    "draw_no": draw_no,
                    "numbers": numbers,
                    "bonus": bonus
                }
            else:
                # API에서 아직 공개되지 않았다는 응답
                print(f"⏳ {draw_no}회차 데이터 없음 (API 응답: {info.get('returnValue')})")
                return None
        except Exception as e:
            print(f"⚠️ {draw_no}회차 요청 오류: {e} (재시도 {attempt+1}/5)")
            time.sleep(2)
    return None

# 새로운 회차부터 자동 추가
added = 0
while True:
    new_draw = fetch_draw(next_draw)
    if not new_draw:
        print(f"🚫 {next_draw}회차는 아직 발표되지 않았거나 가져올 수 없습니다. 종료합니다.")
        break

    data.append(new_draw)
    added += 1
    print(f"✅ {next_draw}회차 추가 완료 → {new_draw['numbers']}")
    next_draw += 1
    time.sleep(1)  # API 부하 방지

# 변경사항이 있으면 저장
if added > 0:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"🎉 총 {added}회차 추가 완료! ({last_draw+1}~{next_draw-1}회차)")
else:
    print("ℹ️ 추가할 회차가 없습니다. (최신 상태)")

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

# 마지막 회차 번호 확인
last_draw = data[-1]["draw_no"] if data else 0
next_draw = last_draw + 1

print(f"🔍 현재 마지막 회차: {last_draw}, 다음 시도 회차: {next_draw}")

# 동행복권 API
url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={next_draw}"

try:
    res = requests.get(url, timeout=5)
    info = res.json()

    # 발표 안 된 회차면 바로 종료
    if info.get("returnValue") != "success":
        print(f"🚫 {next_draw}회차는 아직 발표되지 않음. 종료합니다.")
    else:
        numbers = [
            info[f"drwtNo{i}"] for i in range(1, 7)
        ]
        bonus = info["bnusNo"]

        new_entry = {
            "draw_no": next_draw,
            "numbers": numbers,
            "bonus": bonus
        }

        data.append(new_entry)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ {next_draw}회차 데이터 추가 완료: {numbers} + {bonus}")

except Exception as e:
    print(f"⚠️ 오류 발생: {e}")

print("🟢 업데이트 완료")

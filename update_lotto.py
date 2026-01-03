import json
import os
import requests

file_path = "2025lotto_numbers_1_to_1182_final.json"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

last_draw = data[0]["draw_no"] if data else 0
next_draw = last_draw + 1

# 브라우저인 것처럼 보이게 하는 헤더 추가 (매우 중요)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={next_draw}"

try:
    res = requests.get(url, headers=headers, timeout=10)
    # 응답이 JSON 형태인지 확인
    if res.status_code == 200:
        info = res.json()
        if info.get("returnValue") == "success":
            numbers = [info[f"drwtNo{i}"] for i in range(1, 7)]
            bonus = info["bnusNo"]
            new_entry = {"draw_no": next_draw, "numbers": numbers, "bonus": bonus}
            data.insert(0, new_entry)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ {next_draw}회차 업데이트 성공!")
        else:
            print(f"🚫 {next_draw}회차는 아직 공식 API에 반영되지 않았습니다.")
    else:
        print(f"❌ 서버 응답 오류 (상태 코드: {res.status_code})")
except Exception as e:
    print(f"⚠️ 실행 중 오류가 발생했지만 기록을 중단합니다. (사유: {e})")

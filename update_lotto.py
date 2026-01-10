import json
import os
import requests
import time

# =========================
# 1. JSON 파일 자동 찾기
# =========================
# 현재 폴더에서 .json으로 끝나고 'lotto'라는 이름이 포함된 파일을 찾습니다.
target_file = None
for file in os.listdir('.'):
    if file.endswith('.json') and 'lotto' in file.lower():
        target_file = file
        break

if not target_file:
    print("❌ 로또 JSON 파일을 찾을 수 없습니다. (현재 파일 목록: ", os.listdir('.'), ")")
    exit()

print(f"✅ 파일을 찾았습니다: {target_file}")

# =========================
# 2. 데이터 로드 및 최신 회차 확인
# =========================
with open(target_file, "r", encoding="utf-8") as f:
    data = json.load(f)

existing_draws = {d["draw_no"] for d in data}
next_draw = max(existing_draws) + 1
print(f"🔍 현재 최신: {max(existing_draws)}회 -> 목표: {next_draw}회")

# =========================
# 3. API 호출 및 데이터 추가
# =========================
BASE_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}"
headers = {"User-Agent": "Mozilla/5.0"}

try:
    res = requests.get(BASE_URL.format(next_draw), headers=headers, timeout=10)
    info = res.json()
    
    if info.get("returnValue") == "success":
        # 최신순 정렬을 위해 맨 앞에 삽입
        data.insert(0, {
            "draw_no": next_draw,
            "numbers": [info[f"drwtNo{i}"] for i in range(1, 7)],
            "bonus": info["bnusNo"]
        })
        
        # 파일 저장
        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"🎉 {next_draw}회 업데이트 성공 및 {target_file} 저장 완료!")
    else:
        print(f"ℹ️ {next_draw}회차 데이터가 아직 준비되지 않았습니다.")
except Exception as e:
    print(f"❌ 오류 발생: {e}")

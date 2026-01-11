import json
import os
import requests
import sys

# =========================
# 1. JSON 파일 자동 찾기
# =========================
target_file = None
for file in os.listdir('.'):
    if file.endswith('.json') and 'lotto' in file.lower():
        target_file = file
        break

if not target_file:
    print("❌ 로또 JSON 파일을 찾을 수 없습니다.")
    sys.exit(0)

print(f"✅ 파일 발견: {target_file}")

# =========================
# 2. JSON 로드 (깨졌으면 중단)
# =========================
try:
    with open(target_file, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print("❌ JSON 파일이 손상되었습니다. 수동 복구 필요:", e)
    sys.exit(0)

existing_draws = {d["draw_no"] for d in data}
latest_draw = max(existing_draws)
next_draw = latest_draw + 1

print(f"🔍 최신 회차: {latest_draw} → 다음 회차 시도: {next_draw}")

# =========================
# 3. 동행복권 API 호출
# =========================
BASE_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}"
headers = {"User-Agent": "Mozilla/5.0"}

try:
    res = requests.get(BASE_URL.format(next_draw), headers=headers, timeout=10)
    info = res.json()
except Exception as e:
    print("❌ API 호출 실패:", e)
    sys.exit(0)

# =========================
# 4. 데이터 검증
# =========================
if info.get("returnValue") != "success":
    print(f"ℹ️ {next_draw}회차 데이터 아직 미공개")
    sys.exit(0)

numbers = [info.get(f"drwtNo{i}") for i in range(1, 7)]
bonus = info.get("bnusNo")

if (
    len(numbers) != 6
    or any(n is None for n in numbers)
    or not isinstance(bonus, int)
):
    print("⚠️ 데이터가 완전하지 않아 저장하지 않습니다.")
    sys.exit(0)

# =========================
# 5. 데이터 삽입 (중복 방지)
# =========================
if next_draw in existing_draws:
    print(f"ℹ️ {next_draw}회차는 이미 존재합니다.")
    sys.exit(0)

data.insert(0, {
    "draw_no": next_draw,
    "numbers": numbers,
    "bonus": bonus
})

# =========================
# 6. 안전한 저장 (임시파일 → 교체)
# =========================
tmp_file = target_file + ".tmp"

with open(tmp_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

os.replace(tmp_file, target_file)

print(f"🎉 {next_draw}회차 업데이트 완료!")

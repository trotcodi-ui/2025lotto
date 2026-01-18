import json
from pathlib import Path

# 업데이트할 파일 이름
LOCAL_FILE = Path("2025lotto_numbers_1_to_1182_final.json")

# 1207회 당첨 번호 직접 입력 (image_430726.png 기반)
FIXED_DATA = {
    "draw_no": 1207,
    "numbers": [10, 22, 24, 27, 38, 45],
    "bonus": 11
}

def main():
    if not LOCAL_FILE.exists():
        print("❌ JSON 파일을 찾을 수 없습니다.")
        return

    # 기존 데이터 불러오기
    with open(LOCAL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 중복 확인 및 업데이트
    if data[0]["draw_no"] < FIXED_DATA["draw_no"]:
        data.insert(0, FIXED_DATA)
        with open(LOCAL_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"🎉 {FIXED_DATA['draw_no']}회차 데이터가 성공적으로 저장되었습니다!")
    else:
        print(f"✅ 이미 {data[0]['draw_no']}회차 데이터가 존재합니다.")

if __name__ == "__main__":
    main()

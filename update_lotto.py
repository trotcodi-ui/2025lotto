import requests
import json
import os

# 파일 경로 및 API 주소
LOTTO_JSON_PATH = '2025lotto_numbers_1_to_1182_final.json'
API_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="

def update_lotto_data():
    if os.path.exists(LOTTO_JSON_PATH):
        try:
            with open(LOTTO_JSON_PATH, 'r', encoding='utf-8') as f:
                lotto_data = json.load(f)
        except:
            lotto_data = []
    else:
        lotto_data = []

    last_draw = max([d['draw_no'] for d in lotto_data]) if lotto_data else 0
    target_draw = last_draw + 1

    print(f"현재 최신 회차: {last_draw} / 조회 시도 회차: {target_draw}")

    # 브라우저 위장 헤더 (차단 방지)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(f"{API_URL}{target_draw}", headers=headers, timeout=10)
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get("returnValue") == "success":
                    new_entry = {
                        "draw_no": result["drwNo"],
                        "date": result["drwNoDate"],
                        "numbers": [
                            result["drwtNo1"], result["drwtNo2"], result["drwtNo3"],
                            result["drwtNo4"], result["drwtNo5"], result["drwtNo6"]
                        ],
                        "bonus": result["bnusNo"]
                    }
                    lotto_data.append(new_entry)
                    lotto_data.sort(key=lambda x: x['draw_no'], reverse=True)
                    with open(LOTTO_JSON_PATH, 'w', encoding='utf-8') as f:
                        json.dump(lotto_data, f, ensure_ascii=False, indent=4)
                    print(f"✅ {target_draw}회 업데이트 성공!")
                else:
                    print(f"❌ {target_draw}회차 데이터가 아직 없습니다.")
            except:
                print("⚠️ 서버 응답 해석 실패")
    except Exception as e:
        print(f"❗ 오류 발생: {e}")

if __name__ == "__main__":
    update_lotto_data()

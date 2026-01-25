import requests
import json
import os

# 사용자님이 제공해주신 구글 시트 주소 (CSV 모드로 변환)
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSd2GO5CSmSb7VgZCpGQBFLuHE-MI0b0agXPxSUXFZjo0S2H3CqfbmfIjz3vIpE4C7RJdhfq_MnSbA1/pub?output=csv"
LOTTO_JSON_PATH = '2025lotto_numbers_1_to_1182_final.json'

def update_lotto_data():
    # 1. 기존 데이터 로드
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
    print(f"🎯 구글 시트 우회 방식 가동 - 목표: {target_draw}회")

    try:
        # 2. 구글 시트에서 데이터 읽기
        response = requests.get(GOOGLE_SHEET_CSV_URL, timeout=15)
        if response.status_code == 200:
            # CSV 데이터 파싱 (구글 시트 수식 결과가 한 줄씩 들어옴)
            lines = response.text.strip().split('\n')
            # 숫자만 추출 (수식 결과로 나온 값들)
            extracted_numbers = [line.strip().replace('"', '') for line in lines if line.strip()]
            
            if len(extracted_numbers) >= 7:
                new_entry = {
                    "draw_no": target_draw,
                    "date": "2026-01-24", # 구글 시트에서 날짜까지 가져오도록 확장 가능
                    "numbers": [int(n) for n in extracted_numbers[:6]],
                    "bonus": int(extracted_numbers[6])
                }

                lotto_data.append(new_entry)
                lotto_data.sort(key=lambda x: x['draw_no'], reverse=True)

                with open(LOTTO_JSON_PATH, 'w', encoding='utf-8') as f:
                    json.dump(lotto_data, f, ensure_ascii=False, indent=4)
                print(f"✅ {target_draw}회 업데이트 성공! (구글 시트 우회 완료)")
            else:
                print(f"❌ 구글 시트에서 번호를 충분히 찾지 못했습니다. (현재 개수: {len(extracted_numbers)})")
        else:
            print(f"⚠️ 구글 시트 접근 실패 (상태 코드: {response.status_code})")
    except Exception as e:
        print(f"❗ 오류 발생: {e}")

if __name__ == "__main__":
    update_lotto_data()

import requests
import json
import os

# 1. 구글 시트 웹 게시(CSV) URL 확인 (반드시 '웹에 게시'가 되어 있어야 합니다)
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSd2GO5CSmSb7VgZCpGQBFLuHE-MI0b0agXPxSUXFZjo0S2H3CqfbmfIjz3vIpE4C7RJdhfq_MnSbA1/pub?output=csv"
LOTTO_JSON_PATH = '2025lotto_numbers_1_to_1182_final.json'

def update_lotto_data():
    if os.path.exists(LOTTO_JSON_PATH):
        try:
            with open(LOTTO_JSON_PATH, 'r', encoding='utf-8') as f:
                lotto_data = json.load(f)
        except:
            lotto_data = []
    else:
        lotto_data = []

    try:
        response = requests.get(GOOGLE_SHEET_CSV_URL, timeout=15)
        if response.status_code == 200:
            # CSV 데이터 파싱 (한 줄씩 읽기)
            lines = response.text.strip().split('\n')
            raw_values = [line.strip().replace('"', '') for line in lines if line.strip()]
            
            # [수정 포인트] 숫자가 아닌 값(예: '1208회')을 걸러내고 숫자만 추출
            extracted_numbers = []
            current_draw_no = 0

            for val in raw_values:
                if '회' in val: # "1208회"에서 숫자만 추출
                    current_draw_no = int(''.join(filter(str.isdigit, val)))
                elif val.isdigit():
                    extracted_numbers.append(int(val))

            # 데이터가 충분한지 확인 (회차 정보와 번호 7개)
            if current_draw_no > 0 and len(extracted_numbers) >= 7:
                # 중복 확인: 이미 해당 회차가 있다면 건너뜀
                if any(d['draw_no'] == current_draw_no for d in lotto_data):
                    print(f"ℹ️ {current_draw_no}회 데이터가 이미 존재합니다.")
                    return

                new_entry = {
                    "draw_no": current_draw_no,
                    "date": "2026-01-24", 
                    "numbers": extracted_numbers[:6],
                    "bonus": extracted_numbers[6]
                }

                lotto_data.append(new_entry)
                lotto_data.sort(key=lambda x: x['draw_no'], reverse=True)

                with open(LOTTO_JSON_PATH, 'w', encoding='utf-8') as f:
                    json.dump(lotto_data, f, ensure_ascii=False, indent=4)
                print(f"✅ {current_draw_no}회 업데이트 성공! JSON 저장 완료.")
            else:
                print(f"❌ 데이터를 충분히 찾지 못했습니다. (추출된 숫자: {len(extracted_numbers)}개)")
        else:
            print(f"⚠️ 시트 접근 실패: {response.status_code}")
    except Exception as e:
        print(f"❗ 오류 발생: {e}")

if __name__ == "__main__":
    update_lotto_data()

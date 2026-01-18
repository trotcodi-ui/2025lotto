import requests
import json
import os

# 1. 설정 및 경로
LOTTO_JSON_PATH = '2025lotto_numbers_1_to_1182_final.json'  # 기존 파일명
API_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="

def get_latest_draw_no():
    """현재까지 진행된 최신 회차 번호를 계산합니다."""
    # 로또 1회차 날짜 기준(2002-12-07)으로 현재 날짜를 계산하여 대략적인 최신 회차 추정 가능하나, 
    # 여기서는 데이터 파일의 마지막 번호 + 1부터 조회하는 방식을 사용합니다.
    pass

def update_lotto_data():
    # 기존 데이터 불러오기
    if os.path.exists(LOTTO_JSON_PATH):
        with open(LOTTO_JSON_PATH, 'r', encoding='utf-8') as f:
            lotto_data = json.load(f)
    else:
        lotto_data = []

    # 현재 저장된 최신 회차 확인
    last_saved_draw = max([d['draw_no'] for d in lotto_data]) if lotto_data else 0
    target_draw = last_saved_draw + 1

    print(f"현재 저장된 최신 회차: {last_saved_draw}회")
    print(f"조회 시도 회차: {target_draw}회...")

    # API 호출 (동행복권)
    response = requests.get(f"{API_URL}{target_draw}")
    
    if response.status_code == 200:
        result = response.json()
        
        # 회차 데이터가 실제로 존재하는지 확인 (returnValue가 'success'인 경우)
        if result.get("returnValue") == "success":
            new_draw = {
                "draw_no": result["drwNo"],
                "date": result["drwNoDate"],
                "numbers": [
                    result["drwtNo1"], result["drwtNo2"], result["drwtNo3"],
                    result["drwtNo4"], result["drwtNo5"], result["drwtNo6"]
                ],
                "bonus": result["bnusNo"]
            }
            
            lotto_data.append(new_draw)
            # 회차 순으로 정렬 (내림차순)
            lotto_data.sort(key=lambda x: x['draw_no'], reverse=True)
            
            # 파일 저장
            with open(LOTTO_JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump(lotto_data, f, ensure_ascii=False, indent=4)
            
            print(f"✅ {target_draw}회 데이터 업데이트 완료!")
        else:
            print(f"❌ {target_draw}회차 데이터가 아직 발표되지 않았습니다.")
    else:
        print("⚠️ API 연결에 실패했습니다.")

if __name__ == "__main__":
    update_lotto_data()

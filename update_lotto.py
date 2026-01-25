<pre><code class="language-python">
import requests
import json
import os

# 1. 설정 및 경로
LOTTO_JSON_PATH = '2025lotto_numbers_1_to_1182_final.json'  # 기존 파일명
API_URL = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="

def update_lotto_data():
    # 기존 데이터 불러오기
    if os.path.exists(LOTTO_JSON_PATH):
        try:
            with open(LOTTO_JSON_PATH, 'r', encoding='utf-8') as f:
                lotto_data = json.load(f)
        except json.JSONDecodeError:
            lotto_data = []
    else:
        lotto_data = []

    # 현재 저장된 최신 회차 확인
    last_saved_draw = max([d['draw_no'] for d in lotto_data]) if lotto_data else 0
    target_draw = last_saved_draw + 1

    print(f"현재 저장된 최신 회차: {last_saved_draw}회")
    print(f"조회 시도 회차: {target_draw}회...")

    # 2. 헤더 설정 (브라우저인 척 위장하여 차단 회피)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # API 호출
        response = requests.get(f"{API_URL}{target_draw}", headers=headers)
        
        # 3. 응답 상태 확인 및 JSON 해석 예외 처리
        if response.status_code == 200:
            try:
                result = response.json()
            except requests.exceptions.JSONDecodeError:
                print(f"⚠️ {target_draw}회차 응답이 JSON 형식이 아닙니다. (서버 차단 혹은 점검 중)")
                return

            # 회차 데이터가 실제로 존재하는지 확인
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
                print(f"❌ {target_draw}회차 데이터가 아직 발표되지 않았습니다. (returnValue: fail)")
        else:
            print(f"⚠️ API 연결에 실패했습니다. (상태 코드: {response.status_code})")
            
    except Exception as e:
        print(f"❗ 오류 발생: {e}")

if __name__ == "__main__":
    update_lotto_data()
</code></pre>

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

    # 서버 차단을 뚫기 위한 정교한 브라우저 위장 헤더
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.dhlottery.co.kr/common.do?method=main",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive"
    }

    try:
        # API 요청 (verify=True가 기본이지만 보안 연결 문제를 피하기 위해 추가)
        response = requests.get(f"{API_URL}{target_draw}", headers=headers, timeout=15)
        
        if response.status_code == 200:
            try:
                # 응답 내용 확인
                content = response.text.strip()
                if content.startswith("<!DOCTYPE"):
                    print("⚠️ 서버가 여전히 차단 중입니다. (HTML 에러 페이지 수신)")
                    print(f"서버 응답 앞부분: {content[:100]}")
                    return

                result = response.json()
                if result.get("returnValue") == "success":
                    new_entry = {
                        "draw_no": int(result["drwNo"]),
                        "date": result["drwNoDate"],
                        "numbers": [
                            int(result["drwtNo1"]), int(result["drwtNo2"]), int(result["drwtNo3"]),
                            int(result["drwtNo4"]), int(result["drwtNo5"]), int(result["drwtNo6"])
                        ],
                        "bonus": int(result["bnusNo"])
                    }
                    lotto_data.append(new_entry)
                    lotto_data.sort(key=lambda x: x['draw_no'], reverse=True)
                    
                    with open(LOTTO_JSON_PATH, 'w', encoding='utf-8') as f:
                        json.dump(lotto_data, f, ensure_ascii=False, indent=4)
                    print(f"✅ {target_draw}회 업데이트 성공!")
                else:
                    print(f"❌ {target_draw}회차 데이터가 아직 없습니다.")
            except Exception as e:
                print(f"⚠️ 데이터 해석 실패: {e}")
        else:
            print(f"⚠️ 연결 실패 (상태 코드: {response.status_code})")
    except Exception as e:
        print(f"❗ 요청 중 오류 발생: {e}")

if __name__ == "__main__":
    update_lotto_data()

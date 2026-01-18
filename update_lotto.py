import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

LOCAL_FILE = Path("2025lotto_numbers_1_to_1182_final.json")
# 사용자님이 지목하신 가장 확실한 페이지 주소
TARGET_URL = "https://www.dhlottery.co.kr/lt645/intro"

def main():
    if not LOCAL_FILE.exists():
        print("❌ 저장할 JSON 파일을 찾을 수 없습니다.")
        return

    with sync_playwright() as p:
        # 1. 실제 사람의 크롬 브라우저 환경을 완벽히 재현
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print(f"🌐 지정하신 페이지로 접속 중: {TARGET_URL}")
        try:
            # 2. 페이지 접속 및 전체 로딩 대기
            page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)
            
            # 3. 화면이 안정화될 때까지 7초간 여유 있게 대기 (이미지의 번호 로딩 시간 확보)
            print("⏳ 화면의 번호 정보를 읽기 위해 잠시 기다립니다...")
            time.sleep(7)
            
            # 4. 이미지(image_430726.png)에 보이는 번호 위치에서 데이터 추출
            # 회차 번호 (예: 제1207회)
            draw_no_text = page.locator("div.win_result h4 strong").inner_text()
            draw_no = int(draw_no_text.replace("제", "").replace("회", "").strip())
            
            # 당첨 번호 6개 (황색, 홍색, 청색 등 공 이미지 안의 숫자)
            num_elements = page.locator("div.num.win span.ball_645")
            nums = [int(num_elements.nth(i).inner_text()) for i in range(6)]
            
            # 보너스 번호 (청색 공)
            bonus = int(page.locator("div.num.bonus span.ball_645").inner_text())
            
            new_entry = {"draw_no": draw_no, "numbers": nums, "bonus": bonus}
            print(f"✨ 읽기 성공! 확인된 데이터: {draw_no}회 {nums} + {bonus}")
            browser.close()
            
        except Exception as e:
            print(f"❌ 화면 분석 중 오류 발생: {e}")
            browser.close()
            return

    # 5. 내 제이슨 파일에 기록
    with open(LOCAL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if new_entry["draw_no"] > data[0]["draw_no"]:
        data.insert(0, new_entry)
        with open(LOCAL_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"🎉 {new_entry['draw_no']}회차 업데이트를 완료했습니다!")
    else:
        print(f"✅ 이미 최신 회차({data[0]['draw_no']}회) 정보가 반영되어 있습니다.")

if __name__ == "__main__":
    main()

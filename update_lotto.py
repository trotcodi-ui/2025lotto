import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

LOCAL_FILE = Path("2025lotto_numbers_1_to_1182_final.json")
TARGET_URL = "https://www.dhlottery.co.kr/lt645/intro"

def main():
    if not LOCAL_FILE.exists():
        print("❌ 파일을 찾을 수 없습니다.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 실제 브라우저와 동일한 설정으로 차단 방지
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print(f"🌐 로또 전용 페이지 접속 중: {TARGET_URL}")
        try:
            # 1. 페이지 접속
            page.goto(TARGET_URL, wait_until="load", timeout=60000)
            
            # 2. 화면 안정화를 위해 잠시 대기
            print("⏳ 화면을 읽기 위해 5초간 대기합니다...")
            time.sleep(5)
            
            # 3. 회차 및 번호 추출 (lt645/intro 페이지 전용 선택자)
            # 회차 번호 추출
            draw_no_text = page.locator("div.win_result h4 strong").inner_text()
            draw_no = int(draw_no_text.replace("회", ""))
            
            # 당첨 번호 6개 추출
            num_locators = page.locator("div.num.win span.ball_645")
            nums = [int(num_locators.nth(i).inner_text()) for i in range(6)]
            
            # 보너스 번호 추출
            bonus = int(page.locator("div.num.bonus span.ball_645").inner_text())
            
            new_entry = {"draw_no": draw_no, "numbers": nums, "bonus": bonus}
            print(f"✨ 추출 성공! {draw_no}회: {nums} + {bonus}")
            browser.close()
            
        except Exception as e:
            print(f"❌ 화면 읽기 실패: {e}")
            browser.close()
            return

    # JSON 파일 업데이트
    with open(LOCAL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if new_entry["draw_no"] > data[0]["draw_no"]:
        data.insert(0, new_entry)
        with open(LOCAL_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"🎉 {new_entry['draw_no']}회차 업데이트 완료!")
    else:
        print(f"✅ 최신 상태 유지 중 (현재: {data[0]['draw_no']}회)")

if __name__ == "__main__":
    main()

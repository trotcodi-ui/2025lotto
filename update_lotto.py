import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

LOCAL_FILE = Path("2025lotto_numbers_1_to_1182_final.json")

def main():
    if not LOCAL_FILE.exists():
        print("❌ 파일을 찾을 수 없습니다.")
        return

    with sync_playwright() as p:
        # 실제 사람 브라우저처럼 보이게 설정
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("🌐 동행복권 화면 접속 중...")
        try:
            # 페이지 접속 및 로딩 대기
            page.goto("https://dhlottery.co.kr/common.do?method=main", wait_until="networkidle")
            
            # 번호가 나타날 때까지 최대 10초 대기
            page.wait_for_selector("#lottoDrwNo", timeout=10000)
            time.sleep(3) # 추가로 3초 더 대기 (안정성 확보)

            draw_no = int(page.locator("#lottoDrwNo").inner_text())
            nums = [int(page.locator(f"#drwtNo{i}").inner_text()) for i in range(1, 7)]
            bonus = int(page.locator("#bnusNo").inner_text())
            
            new_entry = {"draw_no": draw_no, "numbers": nums, "bonus": bonus}
            print(f"✨ 확인된 번호: {draw_no}회 - {nums} + {bonus}")
            browser.close()
            
        except Exception as e:
            print(f"❌ 화면 읽기 실패: {e}")
            browser.close()
            return

    # 파일 업데이트 로직
    with open(LOCAL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if new_entry["draw_no"] > data[0]["draw_no"]:
        data.insert(0, new_entry)
        with open(LOCAL_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"🎉 {new_entry['draw_no']}회 업데이트 성공!")
    else:
        print(f"✅ 이미 최신 상태입니다. (현재: {data[0]['draw_no']}회)")

if __name__ == "__main__":
    main()

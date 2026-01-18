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
        # 실제 사람 브라우저와 동일한 환경 설정
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("🌐 동행복권 화면 접속 시작...")
        try:
            # 1. 사이트 접속 (완전히 로딩될 때까지 대기)
            page.goto("https://dhlottery.co.kr/common.do?method=main", wait_until="load", timeout=90000)
            
            # 2. 화면이 뜬 후 5초간 추가로 더 기다림 (매우 중요)
            print("⏳ 화면 안정화를 위해 5초간 대기합니다...")
            time.sleep(5)
            
            # 3. 번호가 적힌 상자가 나타날 때까지 기다림
            page.wait_for_selector("#lottoDrwNo", timeout=20000)

            # 4. 데이터 읽기
            draw_no = int(page.locator("#lottoDrwNo").inner_text())
            nums = [int(page.locator(f"#drwtNo{i}").inner_text()) for i in range(1, 7)]
            bonus = int(page.locator("#bnusNo").inner_text())
            
            new_entry = {"draw_no": draw_no, "numbers": nums, "bonus": bonus}
            print(f"✨ 읽기 성공! {draw_no}회: {nums} + 보너스 {bonus}")
            browser.close()
            
        except Exception as e:
            print(f"❌ 화면 읽기 최종 실패: {e}")
            browser.close()
            return

    # 파일 업데이트 (기존 데이터와 비교)
    with open(LOCAL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if new_entry["draw_no"] > data[0]["draw_no"]:
        data.insert(0, new_entry)
        with open(LOCAL_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"🎉 {new_entry['draw_no']}회차가 성공적으로 기록되었습니다!")
    else:
        print(f"✅ 이미 최신 회차({data[0]['draw_no']}회)가 반영되어 있습니다.")

if __name__ == "__main__":
    main()

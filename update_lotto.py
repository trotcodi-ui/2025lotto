import json
from pathlib import Path
from playwright.sync_api import sync_playwright

LOCAL_FILE = Path("2025lotto_numbers_1_to_1182_final.json")

def main():
    if not LOCAL_FILE.exists():
        print("❌ 파일을 찾을 수 없습니다.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("🌐 동행복권 화면 확인 중...")
        page.goto("https://www.dhlottery.co.kr/common.do?method=main")
        
        try:
            draw_no = int(page.locator("#lottoDrwNo").inner_text())
            nums = [int(page.locator(f"#drwtNo{i}").inner_text()) for i in range(1, 7)]
            bonus = int(page.locator("#bnusNo").inner_text())
            browser.close()
            
            new_entry = {"draw_no": draw_no, "numbers": nums, "bonus": bonus}
        except:
            print("❌ 화면 읽기 실패")
            browser.close()
            return

    with open(LOCAL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if new_entry["draw_no"] > data[0]["draw_no"]:
        data.insert(0, new_entry)
        with open(LOCAL_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"🎉 {new_entry['draw_no']}회 업데이트 성공!")
    else:
        print("✅ 이미 최신입니다.")

if __name__ == "__main__":
    main()

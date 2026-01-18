import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

LOCAL_FILE = Path("2025lotto_numbers_1_to_1182_final.json")

def fetch_lotto_from_screen():
    with sync_playwright() as p:
        # 가상 브라우저 실행 (사람인 척 접속)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()
        
        print("🌐 동행복권 사이트 접속하여 화면 확인 중...")
        page.goto("https://www.dhlottery.co.kr/common.do?method=main", timeout=60000)
        
        try:
            # 화면의 각 위치에서 번호 추출
            draw_no = int(page.locator("#lottoDrwNo").inner_text())
            nums = [
                int(page.locator("#drwtNo1").inner_text()),
                int(page.locator("#drwtNo2").inner_text()),
                int(page.locator("#drwtNo3").inner_text()),
                int(page.locator("#drwtNo4").inner_text()),
                int(page.locator("#drwtNo5").inner_text()),
                int(page.locator("#drwtNo6").inner_text())
            ]
            bonus = int(page.locator("#bnusNo").inner_text())
            
            browser.close()
            return {"draw_no": draw_no, "numbers": nums, "bonus": bonus}
        except Exception as e:
            print(f"❌ 화면 인식 실패: {e}")
            browser.close()
            return None

def main():
    if not LOCAL_FILE.exists():
        print("❌ 파일이 존재하지 않습니다.")
        return

    extracted = fetch_lotto_from_screen()
    if not extracted: return

    with open(LOCAL_FILE, "r", encoding="utf-8") as f:
        local_data = json.load(f)

    if extracted["draw_no"] > local_data[0]["draw_no"]:
        local_data.insert(0, extracted)
        with open(LOCAL_FILE, "w", encoding="utf-8") as f:
            json.dump(local_data, f, ensure_ascii=False, indent=2)
        print(f"🎉 {extracted['draw_no']}회차 화면 인식 및 업데이트 완료!")
    else:
        print("✅ 이미 최신 상태입니다.")

if __name__ == "__main__":
    main()

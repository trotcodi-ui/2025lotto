import requests
import re
from bs4 import BeautifulSoup

def get_latest_lotto():
    url = "https://search.daum.net/search?w=tot&q=로또"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()

    html = res.text

    # 🔹 회차 추출 (예: 1208회)
    round_match = re.search(r'(\d+)회', html)
    if not round_match:
        raise Exception("회차 추출 실패")

    round_no = round_match.group(1)

    # 🔹 번호 추출 (공 아이콘 숫자)
    soup = BeautifulSoup(html, "html.parser")
    balls = soup.select('span[class*="ball"]')

    numbers = []
    for b in balls:
        text = b.get_text(strip=True)
        if text.isdigit():
            numbers.append(int(text))

    if len(numbers) < 7:
        raise Exception(f"번호 부족: {numbers}")

    numbers = numbers[:7]  # 6개 + 보너스

    return {
        "round": round_no,
        "numbers": numbers[:6],
        "bonus": numbers[6]
    }


if __name__ == "__main__":
    lotto = get_latest_lotto()

    print(f"{lotto['round']}회")
    print("당첨번호:", lotto["numbers"])
    print("보너스:", lotto["bonus"])

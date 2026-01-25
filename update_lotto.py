import requests
import re

def get_latest_lotto():
    # 1️⃣ 먼저 동행복권 API 시도
    api_url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=0"

    try:
        r = requests.get(
            api_url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": "https://www.dhlottery.co.kr/"
            },
            timeout=10
        )
        data = r.json()

        if data.get("returnValue") == "success":
            return {
                "round": data["drwNo"],
                "numbers": [
                    data["drwtNo1"],
                    data["drwtNo2"],
                    data["drwtNo3"],
                    data["drwtNo4"],
                    data["drwtNo5"],
                    data["drwtNo6"],
                ],
                "bonus": data["bnusNo"]
            }
    except Exception:
        pass

    # 2️⃣ (백업) Daum 크롤링 – 로컬용
    daum_url = "https://search.daum.net/search?w=tot&q=로또"
    html = requests.get(
        daum_url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10
    ).text

    round_match = re.search(r'(\d+)회', html)
    if not round_match:
        raise Exception("회차 추출 실패 (Daum)")

    round_no = round_match.group(1)
    numbers = list(map(int, re.findall(r'class="ball[^"]*">(\d+)<', html)[:7]))

    return {
        "round": round_no,
        "numbers": numbers[:6],
        "bonus": numbers[6]
    }

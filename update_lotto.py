import json
import requests
from pathlib import Path

JSON_PATH = Path("2025lotto_numbers_1_to_1182_final.json")


def get_latest_lotto_from_api():
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=0"

    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.dhlottery.co.kr/"
        },
        timeout=10
    )

    text = r.text.strip()
    print("API 응답 앞부분:", text[:100])

    # ❌ JSON이 아닐 경우
    if not text.startswith("{"):
        raise Exception("API가 JSON을 반환하지 않음")

    data = json.loads(text)

    if data.get("returnValue") != "success":
        raise Exception("동행복권 API returnValue 실패")

    return {
        "round": int(data["drwNo"]),
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


def get_saved_max_round():
    if not JSON_PATH.exists():
        return 0, []

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    max_round = max(item["round"] for item in data)
    return max_round, data


def save_lotto(data_list, new_lotto):
    data_list = [d for d in data_list if d["round"] != new_lotto["round"]]
    data_list.append(new_lotto)
    data_list.sort(key=lambda x: x["round"])

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

    print(f"✅ {new_lotto['round']}회 저장 완료")


def main():
    saved_round, data_list = get_saved_max_round()
    print("저장된 최신 회차:", saved_round)

    try:
        latest = get_latest_lotto_from_api()
    except Exception as e:
        # ❗ API가 이상하면 Actions 실패시키지 않음
        print("⚠️ API 오류:", e)
        print("⏸ 업데이트 스킵")
        return

    print("API 최신 회차:", latest["round"])

    if latest["round"] > saved_round:
        save_lotto(data_list, latest)
    else:
        print("⏸ 이미 최신 상태")


if __name__ == "__main__":
    main()

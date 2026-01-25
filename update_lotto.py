import csv
import json
import requests
from pathlib import Path
import re
from io import StringIO

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSd2GO5CSmSb7VgZCpGQBFLuHE-MI0b0agXPxSUXFZjo0S2H3CqfbmfIjz3vIpE4C7RJdhfq_MnSbA1/pub?output=csv"
JSON_PATH = Path("2025lotto_numbers_1_to_1182_final.json")


def get_lotto_from_csv():
    r = requests.get(CSV_URL, timeout=10)
    r.raise_for_status()

    csv_text = r.text
    reader = csv.reader(StringIO(csv_text))
    rows = list(reader)

    # A1 = "1208회"
    round_text = rows[0][0]
    round_no = int(re.search(r"\d+", round_text).group())

    # A2~A8 = 번호
    nums = [int(rows[i][0]) for i in range(1, 8)]

    return {
        "round": round_no,
        "numbers": nums[:6],
        "bonus": nums[6]
    }


def get_saved_max_round():
    if not JSON_PATH.exists():
        return 0, []

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    max_round = max(item["round"] for item in data)
    return max_round, data


def save_lotto(data_list, lotto):
    data_list = [d for d in data_list if d["round"] != lotto["round"]]
    data_list.append(lotto)
    data_list.sort(key=lambda x: x["round"])

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

    print(f"✅ {lotto['round']}회 JSON 업데이트 완료")


def main():
    lotto = get_lotto_from_csv()
    saved_round, data_list = get_saved_max_round()

    print("CSV 회차:", lotto["round"])
    print("저장된 회차:", saved_round)

    if lotto["round"] > saved_round:
        save_lotto(data_list, lotto)
    else:
        print("⏸ 이미 최신 상태")


if __name__ == "__main__":
    main()

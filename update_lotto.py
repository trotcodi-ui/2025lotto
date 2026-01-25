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

    reader = csv.reader(StringIO(r.text))
    rows = list(reader)

    # A1: "1208회"
    round_text = rows[0][0]
    draw_no = int(re.search(r"\d+", round_text).group())

    nums = [int(rows[i][0]) for i in range(1, 7)]
    bonus = int(rows[7][0])

    return draw_no, nums, bonus


def load_json():
    if not JSON_PATH.exists():
        return []

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data):
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    draw_no, nums, bonus = get_lotto_from_csv()
    data = load_json()

    saved_draws = {item["draw_no"] for item in data}

    print("CSV 회차:", draw_no)

    if draw_no in saved_draws:
        print("⏸ 이미 저장된 회차")
        return

    new_entry = {
        "draw_no": draw_no,
        "numbers": nums,
        "bonus": bonus
    }

    data.insert(0, new_entry)  # 최신 회차를 맨 위에
    save_json(data)

    print(f"✅ {draw_no}회 JSON 업데이트 완료")


if __name__ == "__main__":
    main()

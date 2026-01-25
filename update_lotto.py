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

    round_text = rows[0][0]  # "1208회"
    round_no = int(re.search(r"\d+", round_text).group())

    nums = [int(rows[i][0]) for i in range(1, 8)]

    return {
        "회차": round_no,
        "번호": nums[:6],
        "보너스": nums[6]
    }


def get_saved_max_round():
    if not JSON_PATH.exists():
        return 0, []

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ✅ 기존 JSON 구조 기준
    max_round = max(item["회차"] for item in data)
    return max_round, data


def save_lotto(data_list, new_item):
    # 중복 회차 제거
    data_list = [d for d in data_list if d["회차"] != new_item["회차"]]
    data_list.append(new_item)

    # 회차 순 정렬
    data_list.sort(key=lambda x: x["회차"])

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

    print(f"✅ {new_item['회차']}회 JSON 업데이트 완료")


def main():
    new_item = get_lotto_from_csv()
    saved_round, data_list = get_saved_max_round()

    print("CSV 회차:", new_item["회차"])
    print("저장된 최신 회차:", saved_round)

    if new_item["회차"] > saved_round:
        save_lotto(data_list, new_item)
    else:
        print("⏸ 이미 최신 상태")


if __name__ == "__main__":
    main()

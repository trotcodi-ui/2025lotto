import json
import requests
from pathlib import Path

JSON_PATH = Path("2025lotto_numbers_1_to_1182_final.json")


# 1️⃣ 공식 API에서 최신 확정 회차 가져오기
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
    r.raise_for_status()
    data = r.json()

    if data.get("returnValue") != "success":
        raise Exception("동행복권 API 실패")

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


# 2️⃣ JSON 파일에서 저장된 최대 회차 구하기
def get_saved_max_round():
    if not JSON_PATH.exists():
        return 0, []

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise Exception("JSON 구조가 list가 아님")

    max_round = max(item["round"] for item in data)
    return max_round, data


# 3️⃣ 신규 회차 저장 (중복 제거)
def save_lotto(data_list, new_lotto):
    # 같은 회차 제거
    data_list = [d for d in data_list if d["round"] != new_lotto["round"]]
    data_list.append(new_lotto)

    # 회차 순 정렬
    data_list.sort(key=lambda x: x["round"])

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

    print(f"✅ {new_lotto['round']}회 JSON 업데이트 완료")


# 4️⃣ 메인 실행
def main():
    latest = get_latest_lotto_from_api()
    saved_round, data_list = get_saved_max_round()

    print("저장된 최신 회차:", saved_round)
    print("API 최신 회차:", latest["round"])

    if latest["round"] > saved_round:
        print("🆕 신규 회차 감지 → 업데이트 진행")
        save_lotto(data_list, latest)
    else:
        print("⏸ 이미 최신 상태 → 업데이트 없음")


if __name__ == "__main__":
    main()

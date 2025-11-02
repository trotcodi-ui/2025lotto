export default async function handler(req, res) {
  try {
    const response = await fetch(
      "https://raw.githubusercontent.com/trotcodi-ui/2025lotto/main/2025lotto_numbers_1_to_1182_final.json"
    );
    if (!response.ok) throw new Error("데이터를 불러올 수 없습니다.");
    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: "서버 오류", details: error.message });
  }
}

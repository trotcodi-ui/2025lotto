// api/lotto.js

export default async function handler(req, res) {
  try {
    // 깃허브 JSON 파일 경로
    const response = await fetch(
      'https://raw.githubusercontent.com/trotcodi-ui/2025lotto/refs/heads/main/2025lotto_numbers_1_to_1182_final.json'
    );

    if (!response.ok) {
      throw new Error('데이터를 불러올 수 없습니다. (' + response.status + ')');
    }

    const data = await response.json();

    // JSON 데이터를 그대로 반환
    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}

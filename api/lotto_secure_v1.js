/* 🤖 LOTTO GO SECURE ENGINE - v1.4 (Tistory Stable)
 * Copyright © 2026 trotcodi-ui
 */

// =====================
// 전역 변수
// =====================
window.lottoData = null;
let lastAnalysisText = "";
let currentPool = [];
let currentRangeLabel = "";
let top6Global = [];
let bottom6Global = [];

const BLOG_URL = decodeURIComponent(window.location.href);

// =====================
// DOM 로드 후 시작
// =====================
document.addEventListener("DOMContentLoaded", () => {
  initApp();
  bindEvents();
});

// =====================
// 이벤트 바인딩 (중요)
// =====================
function bindEvents() {
  const $ = (id) => document.getElementById(id);

  $("btn-analyze")?.addEventListener("click", window.analyzeRange);
  $("btn-re-extract")?.addEventListener("click", window.generateRecommendations);
  $("share-analysis-btn")?.addEventListener("click", window.shareAnalysis);
  $("btn-check-history")?.addEventListener("click", () => window.checkHistory());
}

// =====================
// 앱 초기화
// =====================
async function initApp() {
  const CONFIG_URL = "https://raw.githubusercontent.com/trotcodi-ui/2025lotto/refs/heads/main/allowed_sites.json";
  const JSON_URL   = "https://raw.githubusercontent.com/trotcodi-ui/2025lotto/refs/heads/main/2025lotto_numbers_1_to_1182_final.json";

  try {
    // 🔐 도메인 보안 체크
    const res = await fetch(CONFIG_URL, { cache: "no-store" });
    const config = await res.json();
    const allowed = config.allowed.some(site => location.href.includes(site));

    if (!allowed) {
      alert("🚫 허용되지 않은 도메인입니다.");
      location.replace("https://pogkr.tistory.com");
      return;
    }

    // UI 노출
    const wrapper = document.getElementById("lotto-secure-app-wrapper");
    if (wrapper) wrapper.style.display = "block";

    // 로또 데이터 로드
    const lottoRes = await fetch(JSON_URL);
    const data = await lottoRes.json();
    window.lottoData = data.sort((a, b) => b.draw_no - a.draw_no);

    displayLatestLotto(window.lottoData[0]);
    console.log("✅ lottoData loaded:", window.lottoData.length);

  } catch (e) {
    console.error("❌ init error:", e);
    document.getElementById("analysisResult").innerHTML =
      "<p style='color:red;'>데이터 로드 실패</p>";
  }
}

// =====================
// 유틸 함수
// =====================
window.getBallColor = function (n) {
  if (n <= 10) return "#fbc400";
  if (n <= 20) return "#69c8f2";
  if (n <= 30) return "#ff7272";
  if (n <= 40) return "#aaa";
  return "#b0d840";
};

// =====================
// 최신 회차 표시
// =====================
window.displayLatestLotto = function (latest) {
  document.getElementById("latest-draw-title").innerHTML =
    `⭐ 제 ${latest.draw_no}회 당첨번호 ⭐`;

  document.getElementById("latest-draw-date").innerHTML =
    latest.draw_date ? `(추첨일: ${latest.draw_date})` : "";

  document.getElementById("latest-numbers-wrap").innerHTML =
    latest.numbers.map(n =>
      `<span class="num" style="background:${getBallColor(n)}">${n}</span>`
    ).join("");
};

// =====================
// 통계 분석
// =====================
window.analyzeRange = function () {
  if (!window.lottoData) return alert("데이터 로딩 중입니다.");

  const select = document.getElementById("rangeSelect");
  const val = select.value;
  currentRangeLabel = select.options[select.selectedIndex].text;

  const recent = val === "all"
    ? [...window.lottoData]
    : window.lottoData.slice(0, parseInt(val));

  const freq = {};
  for (let i = 1; i <= 45; i++) freq[i] = 0;
  recent.forEach(d => d.numbers.forEach(n => freq[n]++));

  const sorted = Object.entries(freq).sort((a, b) => b[1] - a[1]);

  top6Global = sorted.slice(0, 6).map(v => +v[0]).sort((a, b) => a - b);
  bottom6Global = sorted.slice(-6).map(v => +v[0]).sort((a, b) => a - b);
  currentPool = sorted.slice(0, 24).map(v => +v[0]);

  document.getElementById("analysisResult").innerHTML = `
    <p><b>🔥 많이 나온 숫자 (${currentRangeLabel})</b></p>
    <div>${top6Global.map(n => `<span class="num hot">${n}</span>`).join("")}</div>
    <p style="margin-top:15px"><b>❄️ 적게 나온 숫자 (${currentRangeLabel})</b></p>
    <div>${bottom6Global.map(n => `<span class="num cold">${n}</span>`).join("")}</div>
    <div id="recContainer"></div>
  `;

  document.getElementById("re-extract-options").style.display = "block";
  generateRecommendations();
};

// =====================
// 추천 번호 생성
// =====================
window.generateRecommendations = function () {
  let pool = [...currentPool];
  const excludeLast = document.getElementById("excludeLastWin").checked;
  const fixed = parseInt(document.getElementById("fixedNumber").value);
  const lastNums = window.lottoData[0].numbers;

  if (excludeLast) pool = pool.filter(n => !lastNums.includes(n));
  if (pool.length < 10) pool = Array.from({ length: 45 }, (_, i) => i + 1);

  let html = `<p><b>✨ 추천 번호 (5세트)</b></p>`;
  lastAnalysisText = `📊 로또 분석 (${currentRangeLabel})\n🔥 ${top6Global.join(", ")}\n❄️ ${bottom6Global.join(", ")}\n\n`;

  for (let i = 1; i <= 5; i++) {
    let pick = [];
    if (fixed >= 1 && fixed <= 45) pick.push(fixed);

    let p = pool.filter(n => !pick.includes(n));
    while (pick.length < 6) {
      pick.push(p.splice(Math.floor(Math.random() * p.length), 1)[0]);
    }

    pick.sort((a, b) => a - b);
    lastAnalysisText += `${i}회차: ${pick.join(", ")}\n`;

    html += `
      <div class="recommend-line">
        ${pick.map(n => `<span class="num blue">${n}</span>`).join("")}
        <button class="mini-btn" onclick="checkHistory([${pick}])">이력조회</button>
      </div>`;
  }

  lastAnalysisText += `\n${BLOG_URL}`;
  document.getElementById("recContainer").innerHTML = html;
  document.getElementById("share-analysis-btn").style.display = "block";
};

// =====================
// 결과 복사
// =====================
window.shareAnalysis = function () {
  navigator.clipboard.writeText(lastAnalysisText)
    .then(() => alert("📋 복사 완료"));
};

// =====================
// 이력 조회
// =====================
window.checkHistory = function (nums = null) {
  if (!nums) {
    nums = document.getElementById("userNumbers").value
      .split(",").map(n => +n.trim()).filter(n => n);
  }
  if (nums.length !== 6) return alert("번호 6개 입력");

  let html = `<b>🔍 조회 번호: ${nums.join(", ")}</b><br>`;
  let count = 0;

  window.lottoData.forEach(d => {
    const hit = d.numbers.filter(n => nums.includes(n));
    if (hit.length >= 4) {
      count++;
      html += `<div class="history-item"><b>${d.draw_no}회</b> (${hit.length}개 적중)</div>`;
    }
  });

  document.getElementById("historyResult").innerHTML =
    count ? html : "<p>적중 이력 없음</p>";
};

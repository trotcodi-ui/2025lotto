/* 🤖 LOTTO GO SECURE ENGINE - v1.2 (Tistory Force-Link Version) */

(async function() {
    // 1. 함수들을 전역(window) 객체에 강제 등록 (어디서든 호출 가능하게)
    window.analyzeRange = analyzeRange;
    window.generateRecommendations = generateRecommendations;
    window.checkHistory = checkHistory;
    window.shareAnalysis = shareAnalysis;

    const CONFIG_URL = "https://raw.githubusercontent.com/trotcodi-ui/2025lotto/refs/heads/main/allowed_sites.json";
    const JSON_URL = "https://raw.githubusercontent.com/trotcodi-ui/2025lotto/refs/heads/main/2025lotto_numbers_1_to_1182_final.json";

    try {
        const res = await fetch(CONFIG_URL, { cache: "no-store" });
        const config = await res.json();
        const isAllowed = config.allowed.some(site => window.location.href.includes(site));

        if (!isAllowed) {
            document.body.innerHTML = `<div style="text-align:center; padding:50px; color:red;">🚫 허용되지 않은 사이트입니다.</div>`;
            return;
        }

        const wrapper = document.getElementById("lotto-secure-app-wrapper");
        if(wrapper) wrapper.style.display = "block";

        const lottoRes = await fetch(JSON_URL);
        window.lottoData = (await lottoRes.json()).sort((a,b) => b.draw_no - a.draw_no);
        
        displayLatestLotto(window.lottoData[0]);
        
        // 2. 버튼 연결 (재시도 로직 추가: 0.5초 간격으로 버튼이 생겼는지 확인)
        let retryCount = 0;
        const linker = setInterval(() => {
            const btn = document.getElementById("btn-analyze");
            if (btn || retryCount > 10) {
                initEventListeners();
                clearInterval(linker); // 버튼 찾으면 중단
            }
            retryCount++;
        }, 500);

    } catch (e) { console.error("초기화 오류:", e); }
})();

// --- 기능 함수들 (기존 로직 유지) ---
function initEventListeners() {
    const btns = {
        "btn-analyze": window.analyzeRange,
        "btn-re-extract": window.generateRecommendations,
        "btn-check-history": () => window.checkHistory(),
        "share-analysis-btn": window.shareAnalysis
    };

    for (const [id, func] of Object.entries(btns)) {
        const el = document.getElementById(id);
        if (el) {
            el.onclick = null; // 기존 onclick 제거
            el.addEventListener("click", (e) => {
                e.preventDefault();
                func();
            });
        }
    }
}

// ... (나머지 getBallColor, displayLatestLotto, analyzeRange 등 함수 내용은 동일하게 유지) ...
// (사용자님이 마지막에 올려주신 JS 코드의 나머지 함수들을 이 아래에 붙여넣으시면 됩니다.)

/**
 * 🤖 BOT NOTICE: This script is protected by copyright law.
 * Copyright © 2026 trotcodi-ui. All rights reserved.
 * Unauthorized copying, modification, or distribution is strictly prohibited.
 * Original Source: https://pogkr.tistory.com
 */

(async function() {
    // 1. 보안 설정: 허용할 도메인 리스트 [cite: 2021-12-21]
    const ALLOWED_DOMAINS = ["tistory.com", "github.io", "vercel.app"];
    const currentHost = window.location.hostname;
    const isAllowed = ALLOWED_DOMAINS.some(domain => currentHost.includes(domain));

    // 2. 리디렉션 로직: 허용되지 않은 곳에서 실행 시 내 블로그로 전송
    if (!isAllowed) {
        alert("⚠️ 보호된 콘텐츠입니다. 원본 페이지로 이동합니다.");
        window.location.replace("https://pogkr.tistory.com"); 
        return;
    }

    // 3. 보안 통과 시 앱 활성화
    const appWrapper = document.getElementById("lotto-secure-app-wrapper");
    if(appWrapper) appWrapper.style.display = "block";

    // 4. 데이터 로드 (기존 JSON 경로 사용)
    const JSON_URL = "https://raw.githubusercontent.com/trotcodi-ui/2025lotto/main/2025lotto_numbers_1_to_1182_final.json";
    
    try {
        const res = await fetch(JSON_URL);
        const d = await res.json();
        window.lottoData = d.sort((a,b) => b.draw_no - a.draw_no);
        displayLatestLotto(window.lottoData[0]);
    } catch (e) {
        console.error("데이터 로드 실패:", e);
    }
})();

/* --- 핵심 로직 함수들 (이곳에 보관하여 보호) --- */

function getBallColor(n) {
    if (n <= 10) return "#fbc400"; if (n <= 20) return "#69c8f2";
    if (n <= 30) return "#ff7272"; if (n <= 40) return "#aaa"; return "#b0d840";
}

function displayLatestLotto(latest) {
    const titleEl = document.getElementById("latest-draw-title");
    const wrapEl = document.getElementById("latest-numbers-wrap");
    const statusEl = document.getElementById("auto-status-text");
    
    if(titleEl) titleEl.innerHTML = `⭐ 제 ${latest.draw_no}회 당첨번호 ⭐`;
    if(statusEl) statusEl.innerText = `현재 제 ${latest.draw_no}회차 데이터 반영 완료`;
    
    let html = "";
    latest.numbers.forEach(n => html += `<span class="num" style="background:${getBallColor(n)};">${n}</span>`);
    if(wrapEl) wrapEl.innerHTML = html;
}

// ... (나머지 analyzeRange, generateRecommendations, checkHistory 함수들도 이 아래에 그대로 복사해서 넣어주세요) ...

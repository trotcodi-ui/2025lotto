/* 🤖 LOTTO GO SECURE ENGINE - v1.3 (Tistory Full Integration)
 * Copyright © 2026 trotcodi-ui. All rights reserved.
 */

// 전역 변수 선언
window.lottoData = null;
let lastAnalysisText = ""; 
let currentPool = [];
let currentRangeLabel = "";
let top6Global = [];
let bottom6Global = [];

const BLOG_URL = decodeURIComponent(window.location.href);

// 1. 보안 확인 및 데이터 초기화 (즉시 실행 함수)
(async function initApp() {
    const CONFIG_URL = "https://raw.githubusercontent.com/trotcodi-ui/2025lotto/refs/heads/main/allowed_sites.json";
    const JSON_URL = "https://raw.githubusercontent.com/trotcodi-ui/2025lotto/refs/heads/main/2025lotto_numbers_1_to_1182_final.json";

    try {
        const res = await fetch(CONFIG_URL, { cache: "no-store" });
        const config = await res.json();
        const isAllowed = config.allowed.some(site => window.location.href.includes(site));

        if (!isAllowed) {
            document.body.innerHTML = `<div style="text-align:center; padding:100px; color:red; font-weight:bold;">🚫 허용되지 않은 도메인입니다.</div>`;
            setTimeout(() => { window.location.replace("https://pogkr.tistory.com"); }, 2000);
            return;
        }

        // 보안 통과 시 앱 노출
        const wrapper = document.getElementById("lotto-secure-app-wrapper");
        if(wrapper) wrapper.style.display = "block";

        // 로또 데이터 로드
        const lottoRes = await fetch(JSON_URL);
        const data = await lottoRes.json();
        window.lottoData = data.sort((a, b) => b.draw_no - a.draw_no);
        
        displayLatestLotto(window.lottoData[0]);

    } catch (e) {
        console.error("앱 초기화 중 오류 발생:", e);
    }
})();

// 2. 핵심 기능을 전역(window) 함수로 노출
window.getBallColor = function(n) {
    if (n <= 10) return "#fbc400"; 
    if (n <= 20) return "#69c8f2";
    if (n <= 30) return "#ff7272"; 
    if (n <= 40) return "#aaa"; 
    return "#b0d840";
};

window.displayLatestLotto = function(latest) {
    const titleEl = document.getElementById("latest-draw-title");
    const dateEl = document.getElementById("latest-draw-date");
    const wrapEl = document.getElementById("latest-numbers-wrap");
    const statusEl = document.getElementById("auto-status-text");

    if(titleEl) titleEl.innerHTML = `⭐ 제 ${latest.draw_no}회 당첨번호 ⭐`;
    if(dateEl) dateEl.innerHTML = latest.draw_date ? `(추첨일: ${latest.draw_date})` : "";
    
    let html = "";
    latest.numbers.forEach(n => html += `<span class="num" style="background:${window.getBallColor(n)};">${n}</span>`);
    if(wrapEl) wrapEl.innerHTML = html;
    if(statusEl) statusEl.innerText = `현재 제 ${latest.draw_no}회차 데이터 반영 완료`;
};

window.analyzeRange = function() {
    if(!window.lottoData) return alert("데이터를 불러오는 중입니다. 잠시만 기다려주세요.");
    const val = document.getElementById("rangeSelect").value;
    currentRangeLabel = document.getElementById("rangeSelect").options[document.getElementById("rangeSelect").selectedIndex].text;
    
    let recent = val === "all" ? [...window.lottoData] : window.lottoData.slice(0, parseInt(val));
    const freq = {}; for(let i=1; i<=45; i++) freq[i]=0;
    recent.forEach(d => d.numbers.forEach(n => freq[n]++));
    
    const sorted = Object.entries(freq).sort((a,b) => b[1]-a[1]);
    top6Global = sorted.slice(0,6).map(v => parseInt(v[0])).sort((a,b)=>a-b);
    bottom6Global = sorted.slice(-6).map(v => parseInt(v[0])).sort((a,b)=>a-b);
    currentPool = sorted.slice(0, 24).map(v => parseInt(v[0]));
    
    let html = `<p style="margin-top:20px; font-weight:bold;">🔥 많이 나온 숫자 (${currentRangeLabel})</p>
                <div>${top6Global.map(n=>`<span class="num hot">${n}</span>`).join("")}</div>
                <p style="margin-top:15px; font-weight:bold;">❄️ 적게 나온 숫자 (${currentRangeLabel})</p>
                <div>${bottom6Global.map(n=>`<span class="num cold">${n}</span>`).join("")}</div>
                <div id="recContainer"></div>`;
    
    document.getElementById("analysisResult").innerHTML = html;
    document.getElementById("re-extract-options").style.display = "block";
    window.generateRecommendations(); 
};

window.generateRecommendations = function() {
    let pool = [...currentPool];
    const excludeLast = document.getElementById("excludeLastWin").checked;
    const fixedNum = parseInt(document.getElementById("fixedNumber").value);
    const lastWinNums = window.lottoData[0].numbers;
    
    if (excludeLast) pool = pool.filter(n => !lastWinNums.includes(n));
    if (pool.length < 10) pool = Array.from({length:45}, (_,i)=>i+1);
    
    let html = `<p style="margin-top:20px; font-weight:bold;">✨ 맞춤 추천번호 (5세트)</p>`;
    let shareText = `📊 로또 분석 결과 (${currentRangeLabel})\n\n🔥 많이 나온 수: ${top6Global.join(", ")}\n❄️ 적게 나온 수: ${bottom6Global.join(", ")}\n\n`;
    if(excludeLast) shareText += `✅ 옵션: 지난주 당첨번호 제외 적용\n`;
    if(!isNaN(fixedNum) && fixedNum >= 1 && fixedNum <= 45) shareText += `✅ 옵션: 내가 넣고 싶은 수 [${fixedNum}] 포함\n`;
    
    shareText += `\n🪄 추천 조합 (5세트):\n`;
    for(let i=1; i<=5; i++) {
        let pick = [];
        if (!isNaN(fixedNum) && fixedNum >= 1 && fixedNum <= 45) pick.push(fixedNum);
        let localPool = [...pool].filter(n => !pick.includes(n));
        while(pick.length < 6 && localPool.length > 0) { 
            pick.push(localPool.splice(Math.floor(Math.random()*localPool.length),1)[0]); 
        }
        const sp = pick.sort((a,b)=>a-b);
        html += `<div class="recommend-line">
                    <div class="recommend-nums">${sp.map(n=>`<span class="num blue">${n}</span>`).join("")}</div>
                    <button class="mini-btn" onclick="window.checkHistory([${sp.join(',')}])">이력조회</button>
                 </div>`;
        shareText += `${i}회차: ${sp.join(", ")}\n`;
    }
    shareText += `\n👇 상세 분석 데이터 보기:\n${BLOG_URL}`;
    lastAnalysisText = shareText; 
    document.getElementById("recContainer").innerHTML = html;
    document.getElementById("share-analysis-btn").style.display = "block";
};

window.shareAnalysis = function() {
    if (!lastAnalysisText) return;
    const copyFunc = (text) => {
        const t = document.createElement("textarea"); t.value = text;
        document.body.appendChild(t); t.select(); document.execCommand('copy'); document.body.removeChild(t);
        alert("📊 분석 결과와 추천번호가 복사되었습니다!");
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(lastAnalysisText).then(() => alert("📊 분석 결과와 추천번호가 복사되었습니다!"))
        .catch(() => copyFunc(lastAnalysisText));
    } else {
        copyFunc(lastAnalysisText);
    }
};

window.checkHistory = function(customNums = null) {
    if(!window.lottoData) return;
    let nums = customNums || document.getElementById("userNumbers").value.split(",").map(n=>parseInt(n.trim())).filter(n=>!isNaN(n));
    if(nums.length !== 6) return alert("6개 번호를 확인하세요.");
    
    let html = `<div style="padding:10px; background:#eee; border-radius:6px; margin-bottom:10px; font-size:14px;"><strong>🔍 조회 번호: ${nums.join(", ")}</strong></div>`;
    let count = 0;
    
    window.lottoData.forEach(d => {
        const hit = d.numbers.filter(n => nums.includes(n));
        if(hit.length >= 4) {
            count++;
            let ballHtml = d.numbers.map(n => {
                const isHit = nums.includes(n);
                return `<span class="num ${isHit ? 'hit-ball' : ''}" style="${!isHit ? 'background:'+window.getBallColor(n) : ''}">${n}</span>`;
            }).join("");
            html += `<div class="history-item"><b>제 ${d.draw_no}회차</b> (${d.draw_date || ''})<br><div style="margin-top:10px;">${ballHtml}</div><div style="margin-top:10px; color:#e74c3c; font-weight:bold;">${hit.length}개 적중!</div></div>`;
        }
    });
    document.getElementById("historyResult").innerHTML = count > 0 ? html : "<p style='padding:20px; text-align:center; color:#999;'>4개 이상 적중 이력이 없습니다.</p>";
    if(customNums) document.getElementById("historySection").scrollIntoView({behavior:'smooth'});
};

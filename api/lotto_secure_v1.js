// 티스토리 HTML 버튼들과 JS 함수를 강제로 연결 (ID 기반 최적화)
function initEventListeners() {
    // 1. 통계 분석 실행 버튼
    const analyzeBtn = document.getElementById('btn-analyze');
    if(analyzeBtn) {
        analyzeBtn.addEventListener("click", function(e) {
            e.preventDefault();
            analyzeRange();
        });
    }

    // 2. 옵션 적용 재추출 버튼
    const reExtractBtn = document.getElementById('btn-re-extract');
    if(reExtractBtn) {
        reExtractBtn.addEventListener("click", function(e) {
            e.preventDefault();
            generateRecommendations();
        });
    }

    // 3. 당첨 이력 확인 버튼
    const historyBtn = document.getElementById('btn-check-history');
    if(historyBtn) {
        historyBtn.addEventListener("click", function(e) {
            e.preventDefault();
            checkHistory();
        });
    }

    // 4. 분석 결과 복사 버튼
    const shareBtn = document.getElementById("share-analysis-btn");
    if(shareBtn) {
        shareBtn.addEventListener("click", function(e) {
            e.preventDefault();
            shareAnalysis();
        });
    }
}

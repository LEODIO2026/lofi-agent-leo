#!/bin/bash
export GEMINI_API_KEY="***REMOVED***"
echo "========================================================="
echo "🌸 [Neon Blossom Lofi] 에이전트 레오 무인 업로드 체인 가동"
echo "실행 시각: $(date)"
echo "========================================================="

# 스크립트가 실행되는 절대 경로로 이동
cd "$(dirname "$0")"

# 1. 영상 합성 실행
echo "[자동화 1단계] 1080p 고화질 영상 합성을 시작합니다..."
python3 asset_generator.py

if [ $? -ne 0 ]; then
    echo "🚨 렌더링 중 치명적 오류 발생. 파이프라인 보호를 위해 자동화를 중단합니다."
    exit 1
fi

# 2. 유튜브 자동 업로드 실행
echo ""
echo "[자동화 2단계] YouTube API 전송 및 배포를 쏘아 올립니다..."
python3 youtube_uploader.py

if [ $? -ne 0 ]; then
    echo "🚨 업로드 중 오류 발생."
    exit 1
fi

echo ""
echo "🎉 모든 자동화 파이프라인 루프가 무사히 종료되었습니다."
echo "========================================================="

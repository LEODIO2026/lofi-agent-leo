#!/bin/bash
# Neon Blossom Lofi - AI 무인 자동화 실행 래퍼 (V6-Pro)
# 이 스크립트는 크론탭(Cron)에서 안전하게 실행되도록 경로와 환경 변수를 설정합니다.

# 1. 작업 디렉토리 이동
cd /Users/leo/Documents/바이브코딩/음악채널에이전트레오

# 2. 필수 환경 변수 주입 (Gemini API 키)
export GEMINI_API_KEY="***REMOVED***"

# 3. 전체 자동화 파이프라인 가동 및 로그 기록
# 실행 결과는 /Users/leo/Documents/바이브코딩/음악채널에이전트레오/automation_log.txt 에서 확인 가능합니다.
./run_automation.sh >> automation_log.txt 2>&1

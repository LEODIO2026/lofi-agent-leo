#!/bin/bash
# Neon Blossom Lofi - Cloud Scheduler 트리거 설정 스크립트 (V6-Pro)

# 맥북 파이썬 충돌 방지를 위한 독립 환경(Miniconda) 지정
export CLOUDSDK_PYTHON="$(dirname "$0")/miniconda/bin/python"
GCLOUD_CMD="$(dirname "$0")/google-cloud-sdk/bin/gcloud"

# 1. 변수 설정
PROJECT_ID="lofi-music-youtube-492204"
REGION="asia-northeast3"
JOB_NAME="lofi-agent"
SCHEDULER_NAME="lofi-daily-automation"
SCHEDULE="0 0 * * *" # UTC 00:00 = 한국 시간(KST) 오전 09:00

echo "========================================================="
echo "🌸 [Agent Leo] 구글 클라우드 스케줄러 무인 자동화 구축"
echo "========================================================="

# 2. 기존 스케줄러 삭제 (중복 생성 방지)
echo "[Step 1] 기존 스케줄러 확인 및 정리..."
$GCLOUD_CMD scheduler jobs delete $SCHEDULER_NAME --location=$REGION --quiet 2>/dev/null 2>&1

# 3. 신규 스케줄러 생성
# Cloud Run Job을 직접 실행하는 HTTP POST 요청을 보냅니다.
echo "[Step 2] 매일 오전 9시(KST) 실행 스케줄을 생성합니다..."
$GCLOUD_CMD scheduler jobs create http $SCHEDULER_NAME \
    --location=$REGION \
    --schedule="$SCHEDULE" \
    --uri="https://${REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/${JOB_NAME}:run" \
    --http-method=POST \
    --oauth-service-account-email="$($GCLOUD_CMD projects describe $PROJECT_ID --format='get(projectNumber)')-compute@developer.gserviceaccount.com" \
    --oauth-token-scope="https://www.googleapis.com/auth/cloud-platform" \
    --quiet

echo ""
echo "🎉 [성공] 완전 무인 자동화 환경 구축 완료!"
echo "➡️  이제 매일 오전 9시에 에이전트가 가동되어,"
echo "➡️  매일 낮 12시에 유튜브 영상이 업로드됩니다."
echo "========================================================="

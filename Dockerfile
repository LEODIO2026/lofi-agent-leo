# [Neon Blossom Lofi] 클라우드 실행용 공식 도커 이미지
# 아티팩트 타입: V7-Cloud-Pro

# 1. 가볍고 강력한 Python 3.10 기반 이미지 선택
FROM python:3.10-slim

# 2. 필수 시스템 라이브러리 설치 (MoviePy & FFmpeg 필수 패키지)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 소스 코드 및 필수 에셋 복사
# .dockerignore에 정의된 대용량 파일 및 보안 정보는 제외됩니다.
COPY . .

# 6. 클라우드 전용 엔트리포인트 실행
# Secret Manager 연동 로직이 담긴 main_cloud.py를 실행합니다.
CMD ["python3", "main_cloud.py"]

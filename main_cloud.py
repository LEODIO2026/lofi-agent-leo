import os
import json
import base64
from google.cloud import secretmanager
import asset_generator
import youtube_uploader

def get_secret(secret_id, project_id="lofi-music-youtube-492204"):
    """
    구글 클라우드 Secret Manager에서 시크릿 값을 가져옵니다.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def main():
    print("🚀 [Agent Leo] Cloud Run Job 가동! 시크릿 정보를 로드합니다...")
    
    try:
        # 1. API 키 및 토큰 로드
        gemini_api_key = get_secret("GEMINI_API_KEY")
        fal_key = get_secret("FAL_KEY")
        token_json_str = get_secret("YOUTUBE_TOKEN_JSON")
        credentials_json_str = get_secret("YOUTUBE_CREDENTIALS_JSON")
        
        # 2. 환경 변수 및 파일 설정
        os.environ["GEMINI_API_KEY"] = gemini_api_key
        os.environ["FAL_KEY"] = fal_key
        
        with open("token.json", "w", encoding="utf-8") as f:
            f.write(token_json_str)
            
        with open("credentials.json", "w", encoding="utf-8") as f:
            f.write(credentials_json_str)
            
        print("✅ 시크릿 로드 및 인증 파일 생성 완료.")
        
        # 3. 자동화 파이프라인 실행
        print("\n--- [Step 1: Asset Generation] ---")
        asset_generator.generate_video()
        
        print("\n--- [Step 2: YouTube Upload] ---")
        youtube_uploader.main()
        
        print("\n🎉 [Agent Leo] 모든 클라우드 작업이 성공적으로 종료되었습니다!")
        
    except Exception as e:
        print(f"❌ [Error] 클라우드 실행 중 오류 발생: {e}")
        raise e

if __name__ == "__main__":
    main()

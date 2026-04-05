import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# YouTube Data API 업로드 권한
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"
    
    if not os.path.exists(client_secrets_file):
        print(f"[Error] {client_secrets_file} 파일이 없습니다. Google Cloud Console에서 OAuth 클라이언트 ID를 발급받아 프로젝트 폴더에 넣어주세요.")
        return

    print("[Agent Leo] YouTube API OAuth 인증 토큰 점검...")
    credentials = None
    
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("[Agent Leo] 기존 인증 토큰 만료. 백그라운드에서 자동 갱신을 수행합니다.")
            credentials.refresh(Request())
        else:
            print("[Agent Leo] 등록된 토큰이 없습니다. 브라우저를 통한 로그인 권한 획득을 시작합니다.")
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            credentials = flow.run_local_server(port=0)
            
        # 다음 무인 실행을 위해 토큰 정보 영구 저장
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())
            print("[Agent Leo] token.json 생성 완료! 이후부터 브라우저 팝업은 영원히 생략됩니다.")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # 메타데이터 로드
    metadata_path = "assets/metadata_01.json"
    if not os.path.exists(metadata_path):
        print(f"[Error] {metadata_path} 메타데이터 파일을 찾을 수 없습니다.")
        return

    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    # 영상 파일 (미리 asset_generator.py 로 렌더링된 mp4)
    video_file = "assets/pilot_video_01.mp4"
    if not os.path.exists(video_file):
        print(f"[Error] {video_file} 파일이 없습니다. 먼저 자산(에셋) 합성 모듈을 실행해 영상을 렌더링해 주세요.")
        return

    print(f"[Agent Leo] 다음 콘텐츠 업로드를 진행합니다: {metadata['title']}")
    
    # 비디오 인서트 요청
    request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {
            "categoryId": "10", # Music category
            "description": metadata["description"],
            "title": metadata["title"],
            "tags": metadata["tags"]
          },
          "status": {
            "privacyStatus": "private", # 예약 업로드를 위해 private 설정 필수
            "publishAt": metadata.get("publishAt"), # AI가 계산한 최적 시간 (UTC ISO 8601)
            "selfDeclaredMadeForKids": False, 
          }
        },
        media_body=MediaFileUpload(video_file)
    )
    
    try:
        response = request.execute()
        print("[Agent Leo] 업로드 완료 성공. 비디오 ID:", response.get("id"))
    except googleapiclient.errors.HttpError as e:
        print("[Error] YouTube API 에러 발생:", e)

if __name__ == "__main__":
    main()

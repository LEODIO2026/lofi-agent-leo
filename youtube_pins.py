import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# 고정 댓글 작성을 위해 필요한 권한
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"
    
    video_id = "86wTq7QrT3o" # 사용자 확인 영상 ID
    comment_text = (
        "Thank you for stopping by the Midnight commute. ✨ The city looks so beautifully lonely when it rains, doesn't it? "
        "What is your favorite late-night escape or memory? I'd love to hear your story below. Take a deep breath and rest well. 🌃🌧️"
    )

    if not os.path.exists(client_secrets_file):
        print(f"[Error] {client_secrets_file} 파일이 없습니다.")
        return

    credentials = None
    # 기존 token.json이 있지만 권한이 다를 수 있으므로 별도의 토큰 파일로 관리하거나 덮어씁니다.
    # 여기서는 고정 댓글 전용 권한을 위해 강제 갱신 프로세스를 거칠 수 있음.
    # 고정 댓글 전용 토큰 파일을 별도로 사용합니다.
    token_file = 'token_pins.json'
    
    if os.path.exists(token_file):
        credentials = Credentials.from_authorized_user_file(token_file, SCOPES)
        
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                print("[Agent Leo] 토큰 만료. 자동 갱신 중...")
                credentials.refresh(Request())
            except Exception as e:
                print(f"[Agent Leo] 토큰 갱신 실패: {e}. 새로 인증을 시작합니다.")
                credentials = None
        
        if not credentials:
            print("[Agent Leo] 새로운 권한(force-ssl) 획득이 필요합니다. 브라우저 인증을 가동합니다.")
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            credentials = flow.run_local_server(port=0)
            
        with open(token_file, 'w') as token:
            token.write(credentials.to_json())

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    print(f"[Agent Leo] 영상(ID: {video_id})에 댓글 작성을 시도합니다...")
    
    try:
        # 1. 댓글 작성
        insert_request = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": comment_text
                        }
                    }
                }
            }
        )
        insert_response = insert_request.execute()
        comment_id = insert_response["snippet"]["topLevelComment"]["id"]
        print(f"✅ 댓글 작성 성공! (ID: {comment_id})")

        # 2. 상단 고정 (Pin)
        print("[Agent Leo] 작성된 댓글을 상단에 고정합니다...")
        pin_request = youtube.comments().setModerationStatus(
            id=comment_id,
            moderationStatus="published",
            pinned=True
        )
        pin_request.execute()
        print("🎉 모든 작업이 완료되었습니다! 댓글이 성공적으로 고정되었습니다.")

    except googleapiclient.errors.HttpError as e:
        print(f"❌ YouTube API 에러 발생: {e}")

if __name__ == "__main__":
    main()

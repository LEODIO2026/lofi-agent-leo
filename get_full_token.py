import os
import json
import google_auth_oauthlib.flow
from google.oauth2.credentials import Credentials

# 유튜브 업로드(Upload), 댓글 관리(Force-SSL), 구글 드라이브(Drive) 권한 합본
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/drive.file"
]

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
    client_secrets_file = "credentials.json"
    token_file = 'token_full.json'
    
    if not os.path.exists(client_secrets_file):
        print(f"[Error] {client_secrets_file} 파일이 없습니다.")
        return

    print("[Agent Leo] 합본 권한(Upload + Comment) 획득을 시작합니다. 브라우저 창을 기다려 주세요.")
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    
    # 포트를 51174로 고정하여 브라우저 자동화가 더 수월하게 합니다.
    credentials = flow.run_local_server(port=51174)
    
    with open(token_file, 'w') as token:
        token.write(credentials.to_json())
    
    print(f"🎉 인증 성공! 합본 토큰이 {token_file}에 저장되었습니다. 이 내용을 복사해 클라우드 시크릿을 업데이트하세요.")

if __name__ == "__main__":
    main()

import json
import googleapiclient.discovery
from google.oauth2.credentials import Credentials

def main():
    with open("secret_token.json", "r") as f:
        creds_data = json.load(f)
    credentials = Credentials.from_authorized_user_info(creds_data)
    
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    
    channel_request = youtube.channels().list(part="snippet", mine=True)
    channel_response = channel_request.execute()
    print("클라우드 시크릿 토큰에 연결된 채널:")
    for ch in channel_response.get("items", []):
        print(f" - 채널 ID: {ch['id']}, 채널명: {ch['snippet']['title']}")

if __name__ == "__main__":
    main()

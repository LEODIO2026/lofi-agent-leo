import os
import shutil
import datetime
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

def archive_local(video_path, video_title):
    """
    영상을 로컬 backups/ 폴더에 날짜와 제목을 포함하여 복사합니다.
    """
    # 프로젝트 루트(음악채널에이전트레오) 폴더 하위에 backups 폴더 생성
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(base_dir, "backups")
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"[Agent Leo] 로컬 백업 디렉토리 생성 완료: {backup_dir}")

    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    # 파일명에 사용할 수 없는 문자 제거
    safe_title = "".join([c for c in video_title if c.isalnum() or c in (" ", "-", "_")]).strip()
    backup_filename = f"{date_str}_{safe_title}.mp4"
    dest_path = os.path.join(backup_dir, backup_filename)

    try:
        shutil.copy2(video_path, dest_path)
        print(f"✅ [Agent Leo] 로컬 백업 성공! 파일: {dest_path}")
        return dest_path
    except Exception as e:
        print(f"❌ [Warning] 로컬 백업 중 오류 발생: {e}")
        return None

def upload_to_drive(credentials, video_path, video_title):
    """
    영상을 구글 드라이브의 특정 폴더(Neon Blossom Backups)에 업로드합니다.
    """
    print("[Agent Leo] 구글 드라이브 업로드를 준비합니다...")
    drive_service = googleapiclient.discovery.build("drive", "v3", credentials=credentials)
    
    folder_name = "Always Lofi"
    folder_id = None
    
    try:
        # 1. 폴더 존재 여부 확인
        query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        response = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        
        if response.get('files'):
            folder_id = response['files'][0]['id']
            print(f"[Agent Leo] 기존 드라이브 폴더 사용: {folder_name} (ID: {folder_id})")
        else:
            # 2. 폴더 생성
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = drive_service.files().create(body=file_metadata, fields='id').execute()
            folder_id = folder.get('id')
            print(f"✅ [Agent Leo] 새 드라이브 폴더 생성 완료: {folder_name} (ID: {folder_id})")

        # 3. 파일 업로드
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        file_metadata = {
            'name': f"{date_str}_NeonBlossom_{video_title}.mp4",
            'parents': [folder_id]
        }
        media = MediaFileUpload(video_path, mimetype='video/mp4', resumable=True)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        
        print(f"🎉 [Agent Leo] 구글 드라이브 백업 성공! (File ID: {file.get('id')})")
        return file.get('id')

    except Exception as e:
        print(f"❌ [Warning] 구글 드라이브 업로드 중 오류 발생: {e}")
        return None

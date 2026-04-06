import os
import sys
import random

# Suppress warnings
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, vfx
from PIL import Image
import time

# PIL 버전 호환성 패치 (Pillow 10.0+ 에서 ANTIALIAS 제거됨)
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.LANCZOS

def generate_nano_banana_image():
    # 1. API 키 환경 변수 확인
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[Error] GEMINI_API_KEY 환경 변수가 설정되어 있지 않습니다.")
        print("터미널에서 'export GEMINI_API_KEY=\"발급받은키\"'를 실행 후 다시 가동해주세요.")
        sys.exit(1)
        
    print("[Agent Leo] Nano Banana (Gemini Image API) 호출을 준비합니다...")
    from google import genai
    from google.genai import types
    
    client = genai.Client(api_key=api_key)
    
    # 대표님 전용 '감성 정점' 테마 난수화 패턴 (보랏빛 감성 유지하며 디테일 변주)
    weather = ["softly raining with petals drifting", "glowing neon mist and gentle drizzle", "light misty drizzle with bokeh sparkles", "falling cherry blossoms through rain and neon"]
    lighting_nuance = ["deep violet and indigo with warm amber accents", "majestic magenta and soft purple", "cyan and tender lavender with golden rim light", "holographic pink and teal with dreamy haze"]
    
    # [확정 테마] 아련한 눈빛 + 러블리 니트 가디건 + 보랏빛 빗줄기 발코니 (Seamless Loop 최적화)
    prompt = (
        f"A masterpiece 16:9 cinematic illustration for a lofi music channel. "
        f"A breathtakingly beautiful female anime protagonist with a wistful, soul-searching, and deeply emotional expression, with a soft and lovely glow. "
        f"She is wearing a lovely, oversized pastel-lavender cozy knit cardigan, looking relaxed and dreamily reflective. "
        f"She is leaning against a rain-soaked neon-lit balcony of a cyberpunk high-rise at night, holding a warm steaming mug. "
        f"Around her, a few glowing fireflies and floating petals add a magical, lovely atmosphere. "
        f"In the background, a sprawling cyberpunk city with {random.choice(lighting_nuance)} neon bokeh, gentle {random.choice(weather)}. "
        f"The composition is perfectly symmetrical and visually seamless, designed for infinite looping. "
        f"Highly detailed raindrops on the railing, stunning contrast between warm interior glow and cool night outside. "
        f"High-fidelity Japanese anime style (Makoto Shinkai/Kyoto Animation aesthetics), lyrical, nostalgic, and emotionally resonant. "
        f"No provocative elements, peak emotional resonance. No text."
    )
    
    print(f"[Agent Leo] 오늘의 테마 프롬프트 추출 완료:\n  -> {prompt}")
    print("[Agent Leo] 구글 데이터센터로 실시간 이미지 생성을 요청합니다. (수 초 소요)")
    
    try:
        # Nano Banana 2 (gemini-3.1-flash-image-preview) 제너레이터 호출
        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=[prompt]
        )
        
        image_path = "assets/branding/Neon_Blossom_Dynamic.png"
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                image.save(image_path)
                print(f"[Agent Leo] Nano Banana 2 이미지 생성 완료 및 다운로드 성공: {image_path}")
                return image_path, prompt
                
        raise Exception("API 응답에서 생성된 이미지 데이터를 찾지 못했습니다.")
        
    except Exception as e:
        print(f"[Error] Nano Banana 이미지 생성 실패: {e}")
        # 생성 서버 에러 시 기존 V2 백업용 배너로 폴백(Fallback) 안전장치
        fallback_path = "assets/branding/Neon_Blossom_Banner.png"
        fallback_prompt = "A cozy lofi cyberpunk balcony during a violet rain."
        print("[Agent Leo] 통신 장애로 대체 백업용 기존 배너를 활용합니다.")
        return fallback_path, fallback_prompt

def generate_veo_video(image_path):
    print("\n[Agent Leo] Veo 3 모델을 통한 비디오 렌더링을 준비합니다...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[Error] GEMINI_API_KEY 환경 변수가 설정되어 있지 않습니다.")
        return None
        
    from google import genai
    from google.genai import types
    
    client = genai.Client(api_key=api_key)
    
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    
    first_image = types.Image(image_bytes=img_bytes, mime_type="image/png")
    
    prompt = (
        "A seamless looping cinematic short clip for a lofi music channel. "
        "A cozy cyberpunk balcony at night with soft violet and pink neon reflections on rain-soaked glass. "
        "Gentle rain falls romantically, cherry blossom petals drift slowly in the breeze. "
        "A beautiful anime girl in a lavender knit cardigan sips from a warm mug, her eyes reflecting the dreamy neon city below. "
        "Tiny glowing fireflies float near her. The scene is deeply emotional, incredibly lovely, and tender. "
        "The animation is smooth and perfectly designed to loop without any visible cut or transition. "
        "Soft cinematic grain, warm bokeh, lofi chillhop animation aesthetics. Seamless loop."
    )
    
    print("[Agent Leo] 구글 데이터센터에 Veo 3 비디오 렌더링을 요청합니다. (수 분 소요)")
    try:
        operation = client.models.generate_videos(
            model="veo-3.1-lite-generate-preview",
            prompt=prompt,
            image=first_image,
        )
        
        while not operation.done:
            print("[Agent Leo] 비디오 렌더링 진행 중... 폴링(10초) 대기합니다.")
            time.sleep(10)
            operation = client.operations.get(operation)
            
        video = operation.response.generated_videos[0]
        veo_video_path = "assets/branding/Neon_Blossom_Veo.mp4"
        client.files.download(file=video.video)
        video.video.save(veo_video_path)
        print(f"[Agent Leo] Veo 3 비디오 다운로드 성공: {veo_video_path}")
        return veo_video_path
        
    except Exception as e:
        print(f"[Error] Veo 3 비디오 처리 중 오류 발생: {e}")
        return None

def apply_ken_burns(image_path, duration):
    """
    정지 이미지에 미세한 줌인(Zoom-in) 효과를 주어 영화 같은 느낌을 부여합니다. (Ken Burns Effect)
    비용 0원으로 프리미엄 감성을 유지하는 핵심 로직입니다.
    루프 지점에서 자연스럽게 이어지도록 Ease-in/out 줌을 적용합니다.
    """
    from moviepy.editor import concatenate_videoclips
    print(f"[Agent Leo] 시네마틱 Ken Burns 루핑 효과 적용 중 (Seamless Loop)...")
    
    loop_dur = 30
    clip = ImageClip(image_path).set_duration(loop_dur)
    # 1.0에서 1.08로 아주 천천히 확대 (처음과 끝이 비슷한 줌 레벨이 되도록)
    clip = clip.resize(lambda t: 1 + 0.08 * (t / loop_dur))
    
    # 전체 오디오 길이에 맞춰 크로스페이드로 부드럽게 루핑
    crossfade_dur = 2.0
    clips = []
    total = 0
    while total < duration:
        c = ImageClip(image_path).set_duration(min(loop_dur, duration - total))
        c = c.resize(lambda t: 1 + 0.08 * (t / loop_dur))
        if clips:
            c = c.crossfadein(crossfade_dur)
        clips.append(c)
        total += loop_dur - crossfade_dur
    
    final_clip = concatenate_videoclips(clips, method="compose", padding=-crossfade_dur)
    return final_clip

def generate_lyria_music():
    print("\n[Agent Leo] Lyria 3 Pro 모델을 통해 Lofi 음악 작곡을 개시합니다...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[Error] GEMINI_API_KEY가 없습니다.")
        return None
        
    from google import genai
    from google.genai import types
    
    client = genai.Client(api_key=api_key)
    
    instruments = ["soft piano and distant vinyl crackle", "warm electric guitar and smooth synth pads", "chill xylophone and acoustic guitar", "deep bass and airy flute"]
    beat_style = ["steady boom-bap drums", "relaxed chillhop beat", "slow ambient percussion", "rhythmic jazz-hop drums"]
    
    prompt = f"A relaxing 2-minute lofi chillhop beat with {random.choice(instruments)} and {random.choice(beat_style)}. Atmospheric, nostalgic, and perfect for studying or sleeping. No vocals."
    
    print(f"[Agent Leo] 오늘의 작곡 프롬프트: {prompt}")
    print("[Agent Leo] 구글 데이터센터에 음악 생성을 요청합니다. (약 30초~1분 소요)")
    
    try:
        response = client.models.generate_content(
            model="lyria-3-pro-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO", "TEXT"],
            ),
        )
        
        if not response:
            raise Exception(" Lyria API로부터 응답을 받지 못했습니다. (None)")

        music_path = "assets/branding/Neon_Blossom_Lyria.mp3"
        audio_data = None
        
        if response.parts:
            for part in response.parts:
                if part.inline_data is not None:
                    audio_data = part.inline_data.data
                    break
        elif response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    audio_data = part.inline_data.data
                    break
                
        if audio_data:
            with open(music_path, "wb") as f:
                f.write(audio_data)
            print(f"[Agent Leo] Lyria 3 음악 생성 및 다운로드 성공: {music_path}")
            return music_path
        else:
            raise Exception("API 응답에서 오디오 바이트를 찾지 못했습니다.")
            
    except Exception as e:
        print(f"[Error] Lyria 3 음악 생성 실패: {e}")
        return None

def generate_seo_metadata(image_prompt, music_style):
    """
    그날의 이미지 테마와 음악 스타일에 맞춰, 
    Gemini 1.5 Flash를 활용해 클릭을 부르는 유튜브 제목, 설명, 태그를 JSON으로 생성합니다.
    """
    print("\n[Agent Leo] AI SEO 화가 출격! 오늘의 메타데이터를 작성합니다...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
        
    from google import genai
    from google.genai import types
    import json
    
    client = genai.Client(api_key=api_key)
    
    system_prompt = (
        "You are a poetic, emotionally intelligent Native English copywriter for a premium Global Lofi music channel called 'Neon Blossom Lofi'. "
        "Your task is to write SEO metadata that feels deeply authentic, atmospheric, and emotionally resonant. "
        "CRITICAL RULES: "
        "1. ALL output MUST be strictly in 100% English. DO NOT output any Korean (한국어) under any circumstances. "
        "2. Return ONLY a valid JSON object with keys: 'title', 'description', 'tags'. "
        "3. The description must feel like a personal, artistic diary entry or a warm invitation to relax. "
        "It should NEVER sound corporate, commercial, or like a marketing pitch. "
        "Include a vivid mood-setting story, describe the chillhop vibe, and gently mention the AI tools used as 'Creative Process'. "
        "4. Title: 50-70 characters, emotional, click-worthy in English. Use an em dash (—) for style."
    )

    user_prompt = (
        f"Generate Native English SEO metadata for today's Neon Blossom Lofi video.\n"
        f"WARNING: The output MUST be 100% in English language. NEVER use Korean.\n\n"
        f"Visual Theme: {image_prompt}\n"
        f"Music Style: {music_style}\n\n"
        f"DESCRIPTION FORMAT (follow this structure exactly):\n"
        f"[1-2 sentences: A poetic, vivid story setting the mood. Describe the rain, the neon lights, and the feeling of midnight solitude in English.]\n\n"
        f"[2-3 sentences: Describe the music — the tempo, the instruments, and the calming vibe. Invite the listener to study, sleep, or relax with us in English.]\n\n"
        f"🎵 Tracklist: 00:00 — Full Mix (No Ads)\n\n"
        f"✨ Behind the Vibe\n"
        f"This space was carefully crafted using AI to bring you the ultimate midnight sanctuary.\n"
        f"Curated by: Leo\n"
        f"Music Engine: Google AI Lyria 3\n"
        f"Mood: Soft chillhop · Cyberpunk aesthetic · Rainy night ambient\n\n"
        f"[Hashtag block: 10-15 hashtags including #lofi #cyberpunk #chillhop #aesthetic #lofigirl #lofihiphop #studymusic #sleepmusic #relaxingmusic #animestyle #neonblossom #midnightvibes]\n\n"
        f"TAGS: Provide 20 high-traffic YouTube search tags as a JSON array."
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json"
            )
        )
        
        metadata_json = json.loads(response.text)
        
        # 최적 업로드 시간 예약 (오늘 저녁 9시 기준)
        from datetime import datetime, timedelta
        now = datetime.now()
        # 오늘 21:00 (KST 기준)으로 설정
        publish_time = now.replace(hour=21, minute=0, second=0, microsecond=0)
        if publish_time < now:
            publish_time += timedelta(days=1)
        
        # ISO 8601 형식 (UTC 기준이므로 뒤에 Z를 붙이거나 오프셋 필요)
        # 유튜브 API는 UTC 형식을 선호함.
        publish_at_utc = (publish_time - timedelta(hours=9)).strftime("%Y-%m-%dT%H:%M:%SZ")
        metadata_json["publishAt"] = publish_at_utc
        
        metadata_path = "assets/metadata_01.json"
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata_json, f, ensure_ascii=False, indent=2)
            
        print(f"[Agent Leo] AI SEO 영문 메타데이터 생성 완료: {metadata_path}")
        print(f"  -> 영문 제목: {metadata_json['title']}")
        print(f"  -> 예약 시간(UTC): {publish_at_utc}")
        return metadata_path
        
    except Exception as e:
        print(f"[Error] AI SEO 생성 실패: {e}")
        return None

def generate_video():
    print("="*60)
    print(" [Agent Leo] V5 Full Generative 비디오 합성 엔진 가동: AI Music & Video ")
    print("="*60)
    
    output_path = "assets/pilot_video_01.mp4"
    audio_path = "assets/source.mp3"
    
    # 0. Lyria 3를 통한 무인 음악 작곡 체인
    generated_audio_path = generate_lyria_music()
    if generated_audio_path and os.path.exists(generated_audio_path):
        audio_path = generated_audio_path
        print("[Agent Leo] Lyria 3 앨범이 완성되어 오늘의 배경음악으로 채택되었습니다.")
    else:
        print("[Agent Leo] 음악 생성 제한 혹은 오류로 인해 기존 백업 오디오(source.mp3)를 폴백합니다.")
    
    if not os.path.exists(audio_path):
        print(f"[Error] {audio_path} 오디오 소스가 없습니다. 먼저 넣어주세요.")
        sys.exit(1)

    # 1. Nano Banana를 통한 최초 1회 동적 이미지 생성
    image_path, visual_prompt = generate_nano_banana_image()
    
    if not os.path.exists(image_path):
        print(f"[Error] {image_path} 배너 이미지가 없습니다.")
        sys.exit(1)

    # 1.5. (선택 사항) Veo 3를 통한 동영상 애니메이션 렌더링
    # 대표님의 비용 절감을 위해 최신 가성비 모델인 'veo-3.1-lite'를 기본으로 사용합니다.
    USE_VEO_GEN = True # 가성비 모델 활성화
    veo_path = None
    if USE_VEO_GEN:
        veo_path = generate_veo_video(image_path)

    # 2. 오디오 및 비디오 병합
    print("[Agent Leo] 오디오 및 에셋 로드 중...")
    try:
        audio_clip = AudioFileClip(audio_path)
        
        if veo_path and os.path.exists(veo_path):
            print("[Agent Leo] Veo MP4 소스를 로드하고 크로스페이드로 자연스럽게 무한 루핑합니다.")
            from moviepy.editor import concatenate_videoclips
            base_clip = VideoFileClip(veo_path)
            veo_dur = base_clip.duration
            crossfade_dur = min(1.5, veo_dur * 0.2)  # 클립 길이의 20% 또는 최대 1.5초
            clips = []
            total = 0
            while total < audio_clip.duration:
                c = VideoFileClip(veo_path).subclip(0, min(veo_dur, audio_clip.duration - total))
                if clips:
                    c = c.crossfadein(crossfade_dur)
                clips.append(c)
                total += veo_dur - crossfade_dur
            visual_clip = concatenate_videoclips(clips, method="compose", padding=-crossfade_dur)
        else:
            # Option B: 초저비용 시네마틱 모션 적용
            visual_clip = apply_ken_burns(image_path, audio_clip.duration)
        
        # 3. AI SEO 메타데이터 실시간 생성 (V6)
        # 오늘의 분위기를 기반으로 제목/설명/태그를 자동 생성합니다.
        generate_seo_metadata(visual_prompt, "Emotional Lofi Chillhop")

        print(f"[Agent Leo] V5-Pro-SEO 물리적 렌더링을 시작합니다. 총 길이: {audio_clip.duration:.1f}초")
        
        video = visual_clip.set_audio(audio_clip)
        video.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )
        print(f"[Agent Leo] V5-Pro-SEO 영상 합성 완벽 종료! 저장 경로: {output_path}")
    except Exception as e:
        print("[Error] 렌더링 도중 에러가 발생했습니다:", e)
        sys.exit(1)

if __name__ == "__main__":
    generate_video()

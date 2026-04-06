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
    
    # [다이내믹 프로젝트] 홈 로파이 테마 씬 리스트
    scenes = [
        # 1. 침대 위 (Midnight Bedroom)
        "She is burrowed in soft, plush lavender bedding on a large bed, holding a warm steaming mug. She is looking at a floating holographic interface, or gazing out a large circular window at a violet neon cityscape at night. Cozy and intimate.",
        # 2.거실 쇼파 (Neon Living Room)
        "She is relaxing deeply on a plush, futuristic dark-grey sofa in a spacious living room, with a steaming mug on the side table. Surrounded by soft-glowing cybernetic indoor plants. A sleek digital record player spins in the corner. Tranquil and serene.",
        # 3. 벽난로 앞 (Cyber Fireplace)
        "She is sitting on a fluffy rug in front of a modern electric fireplace with dancing lavender and blue flames. She is holding a warm mug and looking pensively at the fire. Warm and soul-searching.",
        # 4. 식탁/주방 (Rainy Dining Table)
        "She is sitting at a minimalist black marble dining table with a steaming cup of tea. Through a massive floor-to-ceiling window behind her, a heavy neon-lit downpour is visible. Melancholic and beautiful.",
        # 5. 창가 쉼터 (Window Nook)
        "She is perched on a deep, cushioned windowsill of a high-rise, holding a warm mug. Her forehead is gently pressed against the cold, rain-streaked glass as she watches the flying cars and neon signs below. Cinematic and nostalgic."
    ]
    
    selected_scene = random.choice(scenes)
    
    # [확정 테마] 선택된 장면 + 고정 스타일 가이드 (애니메이션 최적화)
    prompt = (
        f"A masterpiece 16:9 cinematic illustration for a lofi music channel. "
        f"A breathtakingly beautiful female anime protagonist with a wistful, soul-searching expression, soft and lovely glow. "
        f"She is wearing a lovely, oversized pastel-lavender cozy knit cardigan, her hair softly swaying. "
        f"{selected_scene} "
        f"The subject is clearly separated from the background to allow for dynamic animation. "
        f"Around her, a few glowing fireflies and floating petals add a magical, lovely atmosphere. "
        f"In the background, a sprawling cyberpunk city with {random.choice(lighting_nuance)} neon bokeh, gentle {random.choice(weather)}. "
        f"Highly detailed raindrops on the glass and surfaces, stunning contrast between warm interior glow and cool night outside. "
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
        "A hyper-dynamic and seamless looping cinematic animation for a lofi music channel. "
        "The beautiful girl in the lavender cardigan is alive: she slowly blinks her eyes, her hair sways gently in the breeze, "
        "and she takes a slow, deep breath, her shoulders moving up and down slightly. "
        "She gently tilts her head while looking at the neon city, then slowly returns to her exact initial posture. "
        "Steam rises from the mug in a beautiful swirling motion. "
        "Rain falls in the background with glowing neon reflections. "
        "CRITICAL: The animation MUST start and end with the exact same pose to ensure a perfect, invisible loop. "
        "The movement should be rich, fluid, and emotionally expressive. "
        "Lofi chillhop aesthetics, dreamy bokeh, masterpiece quality."
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
    정지 이미지에 '숨쉬는 듯한(Breathing)' 줌 효과를 주어 생동감을 부여합니다.
    단순 선형 줌이 아닌, Sine 파동을 이용한 부드러운 전진/후진 모션을 적용합니다.
    """
    import numpy as np
    from moviepy.editor import concatenate_videoclips
    print(f"[Agent Leo] 시네마틱 'Breathing' 루핑 효과 적용 중 (0원 모드 전용)...")
    
    loop_dur = 20 # 20초 단위의 숨쉬는 루프
    
    def zoom_func(t):
        # 1.0에서 1.05 사이를 부드럽게 오가는 Sine 파동 줌
        zoom = 1.0 + 0.025 * (1 - np.cos(2 * np.pi * t / loop_dur))
        return zoom

    clip = ImageClip(image_path).set_duration(loop_dur)
    clip = clip.resize(zoom_func)
    
    # 전체 오디오 길이에 맞춰 크로스페이드로 루핑
    crossfade_dur = 1.0
    clips = []
    total = 0
    while total < duration:
        c = ImageClip(image_path).set_duration(min(loop_dur, duration - total))
        c = c.resize(zoom_func)
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
        return None, "soft piano lofi chillhop, 75 BPM"
        
    from google import genai
    from google.genai import types
    
    client = genai.Client(api_key=api_key)
    
    instruments = [
        "soft piano and distant vinyl crackle",
        "warm electric guitar and smooth synth pads",
        "chill xylophone and acoustic guitar",
        "deep bass and airy flute",
        "mellow trumpet and soft electric piano",
        "lo-fi guitar and warm cello"
    ]
    beat_style = [
        "steady boom-bap drums",
        "relaxed chillhop beat",
        "slow ambient percussion",
        "rhythmic jazz-hop drums",
        "brushed snare and gentle hi-hats"
    ]
    mood_tag = random.choice([
        "melancholic and introspective",
        "warm and nostalgic",
        "dreamy and romantic",
        "peaceful and meditative",
        "bittersweet and tender"
    ])

    chosen_instrument = random.choice(instruments)
    chosen_beat = random.choice(beat_style)
    music_prompt = (
        f"A relaxing 2-minute lofi chillhop beat with {chosen_instrument} and {chosen_beat}. "
        f"Mood: {mood_tag}. Atmospheric, nostalgic, 75 BPM, perfect for studying or sleeping. No vocals."
    )
    
    print(f"[Agent Leo] 오늘의 작곡 프롬프트: {music_prompt}")
    print("[Agent Leo] 구글 데이터센터에 음악 생성을 요청합니다. (약 30초~1분 소요)")
    
    try:
        response = client.models.generate_content(
            model="lyria-3-pro-preview",
            contents=music_prompt,
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
            return music_path, music_prompt
        else:
            raise Exception("API 응답에서 오디오 바이트를 찾지 못했습니다.")
            
    except Exception as e:
        print(f"[Error] Lyria 3 음악 생성 실패: {e}")
        return None, music_prompt

def generate_seo_metadata(scene_description, music_prompt):
    """
    그날의 실제 생성된 시각적 씨과 음악 뎘을 바탕으로,
    하이퍼퍼스나 Gemini Pro를 통해 감성적인 영문 SEO 메타데이터를 생성합니다.
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
        f"Generate native English SEO metadata for a Neon Blossom Lofi YouTube video.\n"
        f"WARNING: ALL output must be 100% in English. NEVER use Korean.\n\n"
        f"=== TODAY'S VISUAL SCENE ===\n"
        f"{scene_description}\n\n"
        f"=== TODAY'S MUSIC ===\n"
        f"{music_prompt}\n\n"
        f"Using the above scene and music as creative fuel, generate:\n"
        f"1. TITLE: One line, 50-70 chars, emotionally resonant, English only. "
        f"The title should evoke the specific mood of today's scene and music. Use an em dash (\u2014) for style.\n"
        f"2. DESCRIPTION: Follow this exact structure:\n"
        f"   - Opening (2-3 sentences): A poetic, first-person story rooted in the specific scene. "
        f"Draw directly from the visual (e.g., fireplace = warmth; bedroom = late night; window = city lights blurring through rain). Make it deeply atmospheric.\n"
        f"   - Music paragraph (2 sentences): Describe the actual instruments and mood of today's music. "
        f"Invite the listener to use it for studying, sleeping, or relaxing.\n"
        f"   - \U0001f3b5 Tracklist: 00:00 \u2014 Full Mix (No Ads)\n"
        f"   - \u2728 Behind the Vibe (3-4 lines): Soft, warm artistic note. Who curated it, the music engine, the mood. "
        f"Keep it personal and human, never corporate.\n"
        f"   - Hashtag line: 10-15 hashtags relevant to both the scene and music.\n"
        f"3. TAGS: 20 high-traffic English YouTube tags as a JSON array."
    )

    
    try:
        response = client.models.generate_content(
            model="gemini-3.1-pro",
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
        print("[Agent Leo] 폴백: 안전한 영어 기본값을 대신 저장합니다.")
        from datetime import datetime, timedelta
        now = datetime.now()
        publish_time = now.replace(hour=21, minute=0, second=0, microsecond=0)
        if publish_time < now:
            publish_time += timedelta(days=1)
        publish_at_utc = (publish_time - timedelta(hours=9)).strftime("%Y-%m-%dT%H:%M:%SZ")
        fallback = {
            "title": "Rainy Night in Neon City — Lofi Beats to Chill & Dream",
            "description": (
                "The rain taps softly against the window as neon signs blur into the wet streets below. "
                "You don’t need to be anywhere tonight — just here, breathing, resting.\n\n"
                "A gentle blend of 75 BPM chillhop, warm synths, and distant vinyl crackle. "
                "The perfect companion for late-night studying, slow evenings, or drifting off to sleep.\n\n"
                "🎵 Tracklist: 00:00 — Full Mix (No Ads)\n\n"
                "✨ Behind the Vibe\n"
                "This space was carefully crafted to bring you the ultimate midnight sanctuary.\n"
                "Curated by: Leo\n"
                "Music Engine: Google AI Lyria 3\n"
                "Mood: Soft chillhop · Cyberpunk aesthetic · Rainy night ambient\n\n"
                "#lofi #cyberpunk #chillhop #aesthetic #lofigirl #studymusic #sleepmusic #neonblossom #midnightvibes"
            ),
            "tags": ["lofi", "chillhop", "cyberpunk lofi", "study music", "sleep music", "lofi beats",
                     "neon blossom lofi", "midnight vibes", "anime lofi", "lo-fi chill",
                     "lofi girl", "rainy lofi", "coding music", "focus music", "calm music"],
            "publishAt": publish_at_utc
        }
        import json as _json
        with open("assets/metadata_01.json", 'w', encoding='utf-8') as f:
            _json.dump(fallback, f, ensure_ascii=False, indent=2)
        return "assets/metadata_01.json"

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
        
        # 3. AI SEO 메타데이터 실시간 생성 (실제 씼 + 음악 프롬프트 연결)
        generate_seo_metadata(visual_prompt, music_prompt)

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

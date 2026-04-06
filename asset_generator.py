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
    
    # =======================================================
    # 새 컨셉: 고양이를 좋아하는 여자의 하루 일과
    # 스타일: 80~90년대 클래식 일본 애니메이션 감성
    # (키마구레 오렌지로드 / 메종일각 / 초기 지브리)
    # 무드: 로맨스, 아련함, 그리움, 설레임
    # =======================================================

    ART_STYLE = (
        "Classic 1980s-1990s Japanese anime art style, similar to Kimagure Orange Road, Maison Ikkoku, and early Studio Ghibli. "
        "Clean, expressive line art with soft cel-shading. Warm, slightly desaturated color palette with gentle film grain. "
        "Big, soulful eyes filled with deep emotion. Soft lighting, natural and lived-in everyday environments. "
        "NO cyberpunk, NO neon signs, NO sci-fi elements. Purely warm, nostalgic, everyday Japanese aesthetic. "
        "16:9 cinematic composition. No text in the image."
    )

    lighting = random.choice([
        "soft morning light filtering through white curtains",
        "golden afternoon sunlight casting long gentle shadows",
        "overcast rainy day with gentle diffused grey light",
        "warm sunset glow through a wooden window frame",
        "quiet blue dusk with a single desk lamp lit",
        "early spring light with cherry blossom petals drifting softly",
    ])

    scenes = [
        # 1. 아침: 침대에서 눈을 뜨는 그녀
        (
            "A young woman slowly waking up in a cozy single bed, her dark hair fanned across the pillow. "
            "Her fluffy grey-and-white cat is sitting on her chest, staring at her with golden eyes. "
            "White curtains billow softly. A small alarm clock, stacked books, and a cat plushie sit on the nightstand.",
            "waking up with her cat, cozy morning bedroom, warm and drowsy"
        ),
        # 2. 아침: 화장실에서 세수하는 그녀
        (
            "A young woman leaning over a small bathroom sink, splashing water on her face. "
            "Her cat perches on the edge of the sink, watching curiously with tilted head. "
            "A toothbrush in a cup, a small potted plant, and a soft towel are visible. "
            "Her reflection in the round mirror shows a sleepy, gentle face. Soft morning light through a frosted window.",
            "morning routine, cat watching, bathroom mirror, sleepy and gentle"
        ),
        # 3. 아침식사: 혼자서 먹는 토스트
        (
            "A young woman sitting alone at a small wooden kitchen table, eating toast and drinking warm tea. "
            "Her cat sits on the chair beside her, watching her eat with hopeful eyes. "
            "A window shows quiet morning street scenery with a bicycle outside. She looks peaceful and slightly lost in thought.",
            "breakfast alone, cat companion, morning kitchen, quiet and cozy"
        ),
        # 4. 통학: 전철을 기다리는 그녀
        (
            "A young woman standing alone on a quiet train platform, holding her school bag straps and looking down the tracks. "
            "A small cat keychain swings from her bag. Her expression is thoughtful and slightly lonely. "
            "Cherry blossoms drift past. Other commuters are softly blurred in the background.",
            "waiting for the train, station platform, pensive and nostalgic"
        ),
        # 5. 설레임: 우연히 마주친 썸남
        (
            "A young woman frozen mid-step on a narrow residential street, her eyes wide and cheeks flushed pink. "
            "A young man across the way has just looked up from his book and their eyes have unexpectedly met. "
            "Cherry blossom petals fall gently between them. Time seems to have stopped. Her cat charm swings from her bag. "
            "The moment is electric, tender, and fleeting.",
            "unexpected eye contact with a crush, heart flutter, romantic and shy"
        ),
        # 6. 학교: 수업 중 딴 생각에 잠긴 그녀
        (
            "A young woman sitting at a school desk, her chin resting on one hand. "
            "She is gazing dreamily out the classroom window at the sky and cherry blossoms, completely lost in her own world. "
            "Her open notebook has a small cat doodle in the corner. The teacher writes on the blackboard in the soft background. "
            "The afternoon light falls warmly across her face.",
            "daydreaming in class, looking out the window, nostalgic school scene"
        ),
        # 7. 저녁: 집으로 걸어오는 그녀
        (
            "A young woman walking home alone in the early evening, earbuds in, hands tucked in her jacket pockets. "
            "A stray cat walks beside her along the low stone wall of a quiet residential street. "
            "The sky is a deep orange and lilac gradient. She has a soft, bittersweet expression, as if thinking of someone.",
            "walking home at dusk, stray cat companion, bittersweet and wistful"
        ),
        # 8. 심야: 창가에 앉아 감성에 빠진 그녀
        (
            "A young woman sitting on a window ledge at night, her cat curled warmly in her lap. "
            "She is looking out at the quiet neighbourhood below, a cup of warm tea held in both hands. "
            "The room behind her is dim and intimate with a desk lamp, stacked books, and a small cat figurine on the shelf. "
            "Her expression is soft, longing, and deeply emotional.",
            "late night by the window, cat in lap, warm tea, longing and emotional"
        ),
    ]

    selected_scene, scene_mood = random.choice(scenes)

    prompt = (
        f"{ART_STYLE} "
        f"Scene: {selected_scene} "
        f"Lighting: {lighting}. "
        f"Mood: {scene_mood}. "
        f"The girl has dark shoulder-length hair, big expressive eyes, and a warm, gentle presence. "
        f"The cat has a distinctive, adorable design and appears as her constant companion."
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
                print(f"[Agent Leo] 이미지 생성 완료: {image_path}")
                return image_path, prompt, scene_mood
                
        raise Exception("API 응답에서 생성된 이미지 데이터를 찾지 못했습니다.")
        
    except Exception as e:
        print(f"[Error] Nano Banana 이미지 생성 실패: {e}")
        # 생성 서버 에러 시 기존 V2 백업용 배너로 폴백(Fallback) 안전장치
        fallback_path = "assets/branding/Neon_Blossom_Banner.png"
        fallback_prompt = "A girl sitting by the window with her cat, holding warm tea, nostalgic and soft."
        fallback_mood = "nostalgic and warm"
        print("[Agent Leo] 이미지 생성 실패. 폴백 배너를 사용합니다.")
        return fallback_path, fallback_prompt, fallback_mood

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
        "A seamless looping cinematic animation in classic 1980s-1990s Japanese anime style (Kimagure Orange Road, early Studio Ghibli). "
        "The girl is gently alive: she blinks slowly, her dark hair sways softly in the breeze, "
        "and her shoulders rise and fall with a quiet, deep breath. "
        "If she has a cat, its tail flicks lazily and one ear twitches. "
        "If she holds a cup of tea, a soft wisp of steam curls upward. "
        "If she is near a window, the curtains billow very gently. "
        "CRITICAL: The animation MUST start and end with the EXACT same pose for a perfect, invisible seamless loop. "
        "All movement is subtle, tender, and emotionally expressive - like a living watercolor painting. "
        "Warm, nostalgic Japanese lofi animation aesthetics. Masterpiece quality."
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
        "You are a poetic, emotionally intelligent Native English copywriter for a cozy, romantic lofi music channel called 'Neon Blossom Lofi'. "
        "The channel follows a young woman who loves cats through her daily life: mornings, commutes, school, chance encounters with a crush, quiet evenings. "
        "The overall feeling is: romance, wistfulness, longing, and gentle flutter. Like reading someone's diary. "
        "CRITICAL RULES: "
        "1. ALL output MUST be strictly in 100% English. DO NOT output any Korean (한국어) under any circumstances. "
        "2. Return ONLY a valid JSON object with keys: 'title', 'description', 'tags'. "
        "3. The description must read like a tender, poetic moment from the girl's day — personal and warm, NEVER corporate or AI-sounding. "
        "4. Title: 50-70 characters, emotionally resonant English. Use an em dash (—) for style."
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
    generated_audio_path, music_prompt = generate_lyria_music()
    if generated_audio_path and os.path.exists(generated_audio_path):
        audio_path = generated_audio_path
        print("✅ [Agent Leo] Lyria 3 음악 생성 완료. SEO에 음악 분위기 연결됩니다.")
    else:
        print("[Agent Leo] 음악 생성 실패. 백업 오디오(source.mp3)를 폴백합니다.")

    
    if not os.path.exists(audio_path):
        print(f"[Error] {audio_path} 오디오 소스가 없습니다. 먼저 넣어주세요.")
        sys.exit(1)

    # 1. Nano Banana를 통한 최초 1회 동적 이미지 생성
    image_path, visual_prompt, scene_mood = generate_nano_banana_image()
    
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

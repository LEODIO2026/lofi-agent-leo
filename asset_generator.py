import os
import sys
import random

# Suppress warnings
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, vfx
from PIL import Image
import time
import requests
import fal_client

# PIL 버전 호환성 패치 (Pillow 10.0+ 에서 ANTIALIAS 제거됨)
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.LANCZOS

# =======================================================
# 전역 설정 0: 채널 정체성 (Identity - Global Edition)
# =======================================================
CHANNEL_NAME = "Always Lofi"
SLOGAN = "Your daily life always needs Lofi."

# =======================================================
# 전역 설정 1: 시네마틱 '2D 시네마틱 애니메이션' 스타일 (Midnight Edition)
# =======================================================
ART_STYLE = (
    "A world-class modern 2D Japanese anime illustration in high-end cinematic style. "
    "VISUAL RULES: Crispy clean line art, sharp hard cel-shading with clear shadow boundaries. NO 3D render feel. "
    "LIGHTING: Gorgeous cinematic lighting contrast - warm indoor yellow glow from lamps vs cool blue/midnight indigo night city outside. "
    "High-end neon signs and city lights visible through the window with realistic 2D glows. "
    "Overall Mood: Sophisticated, urban, calm, and intellectually cozy. Masterpiece quality."
)

# =======================================================
# 전역 설정 2: 캐릭터 DNA (Midnight Edition - New Standards)
# =======================================================
CHARACTER_DESCRIPTION = (
    "Subject: A beautiful and calm young woman with long, straight obsidian black hair. "
    "She has expressive dark almond-shaped eyes and a gentle intellectual aura. "
    "She wears a comfortable modern grey or dark sweater. "
    "Her constant companion is a sleek Siamese cat (color-pointed cat) with a cream-colored body, "
    "dark brown face and ears, and striking blue eyes."
)

# =======================================================
# 전역 설정 3: 일상의 10가지 순간 (Hybrid Master List)
# =======================================================
LIFESTYLE_SCENES = [
    {"subject": "focusing intensely on her books at a wooden desk at night. A desk lamp lit, steam rising from mug", "lighting": "warm yellow indoor vs blue moonlit night", "mood": "deep focus"},
    {"subject": "happily organizing her bookshelf in a sun-drenched sunroom. Dust motes dancing", "lighting": "golden afternoon cinematic rays", "mood": "peaceful cleaning"},
    {"subject": "sitting on the floor eating a bowl of hot ramen. TV glow lighting her face", "lighting": "TV glow in a dark room", "mood": "midnight snack"},
    {"subject": "leaning her head against a rainy bus window. Earphones in", "lighting": "quiet blue dusk with neon blur", "mood": "moody commute"},
    {"subject": "walking through a quiet narrow neighborhood alleyway. Lamp posts glowing", "lighting": "dusk streetlights and night sky", "mood": "evening stroll"},
    {"subject": "resting her chin on her hand, looking at a cherry blossom garden", "lighting": "soft spring daylight with drifting petals", "mood": "daydreaming"},
    {"subject": "chopping vegetables in a bright kitchen. Sunbeams on the cutting board", "lighting": "bright morning kitchen light", "mood": "domestic bliss"}
]

def generate_fal_image(prompt):
    """
    fal.ai (Grok Imagine) API를 사용하여 고품질 이미지를 생성합니다.
    """
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        return None, None
    
    print(f"[Agent Leo] fal.ai (Grok Imagine) 엔진 가동 중...")
    try:
        fal_client.api_key = api_key
        # fal.ai 라이브러리의 subscribe를 사용하여 큐 대기 및 결과 도출
        result = fal_client.subscribe(
            "xai/grok-imagine-image",
            arguments={
                "prompt": prompt,
                "image_size": "landscape_16_9" # [Grok Edition] 16:9 와이드로 전환
            },
            with_logs=True
        )
        
        if "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            image_path = "assets/branding/Neon_Blossom_Dynamic.png"
            
            # 이미지 다운로드
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ [Agent Leo] fal.ai (Grok) 16:9 이미지 생성 성공: {image_path}")
                return image_path, image_url
            
    except Exception as e:
        print(f"[Warning] fal.ai 엔진 일시적 장애: {e}")
    
    return None, None

def generate_fal_video(image_url, prompt):
    """
    fal.ai (Grok Imagine Video) API를 사용하여 이미지를 기반으로 동영상을 생성합니다.
    (Reference-to-Video 기술 적용)
    """
    api_key = os.environ.get("FAL_KEY")
    if not api_key or not image_url:
        return None
    
    print(f"[Agent Leo] fal.ai (Grok Video) 렌더링 중... (Reference-to-Video)")
    try:
        fal_client.api_key = api_key
        # Grok Video Reference-to-Video 모델 호출
        result = fal_client.subscribe(
            "xai/grok-imagine-video/reference-to-video",
            arguments={
                "prompt": f"Cinematic 2D animation movement based on @Image1. {prompt}",
                "reference_image_urls": [image_url],
                "resolution": "720p" # 유튜브 고화질을 위해 720p 베이스
            },
            with_logs=True
        )
        
        if "video" in result:
            video_url = result["video"]["url"]
            video_path = "assets/branding/Neon_Blossom_Grok_Video.mp4"
            
            # 비디오 다운로드
            response = requests.get(video_url)
            if response.status_code == 200:
                with open(video_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ [Agent Leo] fal.ai (Grok Video) 렌더링 성공: {video_path}")
                return video_path
                
    except Exception as e:
        print(f"[Warning] fal.ai 비디오 엔진 일시적 장애: {e}")
    
    return None

def generate_nano_banana_image(prompt, scene_mood):
    """
    구글 Gemini Image (Nano Banana) 모델을 사용하여 이미지를 생성합니다.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[Error] GEMINI_API_KEY 환경 변수가 설정되어 있지 않습니다.")
        return "assets/branding/Neon_Blossom_Banner.png", "Error Prompt", "Default"
        
    print("[Agent Leo] Nano Banana (Gemini Image API) 호출을 준비합니다...")
    from google import genai
    from google.genai import types
    
    client = genai.Client(api_key=api_key)
    
    print(f"[Agent Leo] 오늘의 테마 프롬프트 추출 완료:\n  -> {prompt}")
    print("[Agent Leo] 구글 데이터센터로 실시간 이미지 생성을 요청합니다. (수 초 소요)")
    
    try:
        # Nano Banana 2 (gemini-3.1-flash-image-preview) 16:9 와이드 설정으로 호출
        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=[prompt],
            config=types.GenerateContentConfig(
                output_mime_type="image/png",
                # aspect_ratio="16:9" # 주의: 일부 프리뷰 모델은 config 대신 프롬프트로 제어할 수도 있음
            )
        )
        
        # 프롬프트에 16:9 명시 (가장 확실한 방법)
        prompt_wide = f"{prompt} Aspect Ratio: Cinematic Wide 16:9."
        
        image_path = "assets/branding/Neon_Blossom_Dynamic.png"
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                image.save(image_path)
                print(f"✅ Nano Banana 이미지 생성 및 저장 완료: {image_path}")
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
        f"A cinematic animation in the exact Painterly style of the provided image. "
        "ANIMATION RHYTHM: Limited animation style, animated on 2s (12 unique drawings per second) for a classic 'stepped' cinematic rhythm. "
        "VISUAL QUALITY: Keep the soft bloom and hyper-detailed painterly textures. "
        "MOVEMENT: The girl blinks with character-driven 2D timing, her hair sways in gentle rhythmic increments, and her breathing has the 'frame-by-frame' cadence of a high-end anime film. "
        "CRITICAL: NO smooth 3D interpolation. The motion must NOT look like a 3D render. It must feel like a sequence of hand-painted masterpieces brought to life with 24fps cinematic soul. "
        "Loop perfectly with matching start and end frames."
    )
    
    print("[Agent Leo] 구글 데이터센터에 Veo 3 비디오 렌더링을 요청합니다. (수 분 소요)")
    try:
        operation = client.models.generate_videos(
            model="veo-3.1-lite-generate-preview",
            prompt=prompt,
            image=first_image,
            config=types.GenerateVideoConfig(
                aspect_ratio="16:9",
                resolution="720p"
            )
        )
        
        while not operation.done:
            print("[Agent Leo] 비디오 렌더링 진행 중... 폴링(10초) 대기합니다.")
            time.sleep(10)
            operation = client.operations.get(operation)
            
        video_response = getattr(operation, 'response', None)
        if video_response and hasattr(video_response, 'generated_videos') and video_response.generated_videos:
            video = video_response.generated_videos[0]
            veo_video_path = "assets/branding/Neon_Blossom_Veo.mp4"
            client.files.download(file=video.video)
            video.video.save(veo_video_path)
            print(f"[Agent Leo] Veo 3 비디오 다운로드 성공: {veo_video_path}")
            return veo_video_path
        else:
            error_details = getattr(operation, 'error', '알 수 없는 이유로 응답이 비어있습니다.')
            print(f"[Warning] Veo 3 비디오 생성 스킵: {error_details}")
            return None
            
    except Exception as e:
        print(f"[Error] Veo 3 비디오 처리 중 예외 발생: {e}")
        return None

def apply_vintage_vfx(image_path):
    """
    이미지에 80년대 VHS 애니메이션 감성의 빈티지 효과를 적용합니다.
    (Downscale/Upscale, Chromatic Aberration, Film Grain, Gaussian Softness)
    """
    from PIL import Image, ImageFilter, ImageEnhance, ImageChops
    import numpy as np
    
    print(f"[Agent Leo] 📺 '빈티지 레트로' 필터를 적용 중입니다...")
    
    img = Image.open(image_path).convert("RGB")
    original_size = img.size # 보통 (1920, 1080)
    
    # 1. 의도적인 화질 저하 (불필요한 경우 해제 가능)
    # 이미지가 너무 뿌옇다면 이 과정을 건너뜁니다.
    # low_res_size = (original_size[0] // 2, original_size[1] // 2)
    # img = img.resize(low_res_size, Image.BILINEAR)
    # img = img.resize(original_size, Image.BILINEAR)
    
    # 2. 크로매틱 애버레이션 (색 번짐 효과)
    # R, G, B 채널을 각각 아주 살짝 어긋나게 합성하여 아날로그 느낌을 줍니다.
    r, g, b = img.split()
    r = ImageChops.offset(r, -1, -1)
    b = ImageChops.offset(b, 1, 1)
    img = Image.merge("RGB", (r, g, b))
    
    # 3. 필름 그레인 (미세 노이즈)
    # 화면 전체에 아주 미세한 입자감을 추가합니다.
    np_img = np.array(img).astype(np.float32)
    noise = np.random.normal(0, 4, np_img.shape).astype(np.float32)
    np_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(np_img)
    
    # 4. 미세한 소프트니스 (Gaussian Blur) - 대폭 낮춤
    # 렌즈 필터를 낀 듯한 아주 미세한 따뜻함만 남깁니다.
    img = img.filter(ImageFilter.GaussianBlur(radius=0.1))
    
    # 5. 대비 및 채도 미세 조정 (빈티지 톤)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.05)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.1)

    # 6. 임시 경로 처리 (원본 보존을 위해 파일명 구분)
    filename = os.path.basename(image_path)
    vfx_path = f"assets/branding/vfx_{filename}"
    img.save(vfx_path)
    return vfx_path

def generate_branding_assets():
    """
    유튜브 채널 배너와 프로필 아바타 이미지를 '골든 스타일'로 생성합니다.
    """
    import os
    
    # 1. 유튜브 배너 (Safe Area Precision 16:9)
    # 유튜브 규격(2560x1440) 중 중앙 1546x423 영역이 모든 기기 공통 노출 영역임.
    banner_prompt = (
        f"{ART_STYLE} {CHARACTER_DESCRIPTION} Sitting together in the center. "
        "CRITICAL COMPOSITION: Keep the girl and cat strictly in the HORIZONTAL and VERTICAL CENTER of the frame. "
        "The surrounding top and bottom areas should be filled with beautiful midnight night sky and room floor details. "
        "Main subjects must fit within the center 1/3 height of the image to ensure mobile/desktop visibility. "
        "Cinematic wide shot, night city bloom, 35mm film grain, 16:9 widescreen masterpiece."
    )
    
    print("\n[Agent Leo] 🎨 [Grok] 유튜브 배너 이미지를 생성 중 (16:9)...")
    banner_raw, _ = generate_fal_image(banner_prompt)
    if banner_raw:
        # 파일명 변경 (원본 보존)
        os.rename(banner_raw, "assets/branding/youtube_banner_raw.png")
        banner_raw = "assets/branding/youtube_banner_raw.png"
    
    # 2. 유튜브 프로필 (Square/Expressive 1:1)
    avatar_prompt = (
        f"{ART_STYLE} {CHARACTER_DESCRIPTION} An emotional medium close-up shot focusing on the girl and her Siamese cat. "
        "Gentle interaction, warm indoor lighting against a cool blue night window. "
        "Sparkling almond eyes, detailed hair, soft bokeh background. Masterpiece cinematic OVA."
    )
    
    print("[Agent Leo] 🌸 [Grok] 유튜브 프로필 이미지를 생성 중 (1:1)...")
    # 1:1을 위해 새 임시 프롬프트로 호출 (기본이 square일 가능성이 높음)
    avatar_raw, _ = generate_fal_image(avatar_prompt) 
    if avatar_raw:
        os.rename(avatar_raw, "assets/branding/youtube_avatar_raw.png")
        avatar_raw = "assets/branding/youtube_avatar_raw.png"
        
    # 빈티지 필터 적용
    banner_vfx = apply_vintage_vfx(banner_raw)
    avatar_vfx = apply_vintage_vfx(avatar_raw)
    
    # 최종 파일명으로 정리
    os.replace(banner_vfx, "assets/branding/youtube_banner.png")
    os.replace(avatar_vfx, "assets/branding/youtube_avatar.png")
    
    print(f"\n✅ 브랜딩 에셋 생성 완료!")
    print(f"   -> 배너: assets/branding/youtube_banner.png")
    print(f"   -> 프로필: assets/branding/youtube_avatar.png")

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

def generate_lyria_music(image_path=None):
    print("\n[Agent Leo] Lyria 3 Pro 모델을 통해 Lofi 음악 작곡을 개시합니다...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[Error] GEMINI_API_KEY가 없습니다.")
        return None, "soft piano lofi chillhop, 75 BPM"
        
    from google import genai
    from google.genai import types
    
    client = genai.Client(api_key=api_key)
    
    instruments = [
        "soft jazz piano and warm vinyl crackle",
        "smooth saxophone and mellow synth pads",
        "upright bass and acoustic guitar",
        "mellow trumpet and soft jazz chords",
        "warm electric guitar and electric piano",
        "chill xylophone and jazzy upright bass"
    ]
    beat_style = [
        "rhythmic jazz-hop drums",
        "relaxed chillhop beat with swing",
        "subtle jazzy breakbeats",
        "steady boom-bap jazz drums",
        "brushed snare and gentle hi-hats"
    ]
    mood_tag = random.choice([
        "melancholic and introspective",
        "warm and nostalgic",
        "dreamy and romantic",
        "peaceful and meditative",
        "sophisticated and jazzy"
    ])

    chosen_instrument = random.choice(instruments)
    chosen_beat = random.choice(beat_style)
    music_prompt = (
        f"A relaxing 2-minute jazzy lofi chillhop beat with {chosen_instrument} and {chosen_beat}, "
        "featuring sophisticated jazzy harmonies and a calm urban vibe. "
        f"Mood: {mood_tag}. Atmospheric, nostalgic, 75 BPM, perfect for studying or sleeping. No vocals."
    )
    
    # 멀티모달 콘텐츠 구성
    contents = [f"An atmospheric lofi chillhop track inspired by the mood and colors in this image. {music_prompt}"]
    
    if image_path and os.path.exists(image_path):
        print(f"[Agent Leo] 🖼️ 생성된 이미지의 감성을 분석하여 작곡에 반영합니다...")
        img = Image.open(image_path)
        contents.append(img)
        
    print(f"[Agent Leo] 오늘의 작곡 프롬프트: {music_prompt}")
    print("[Agent Leo] 구글 데이터센터에 음악 생성을 요청합니다. (약 30초~1분 소요)")
    
    music_path = "assets/branding/Neon_Blossom_Lyria.mp3"
    
    try:
        response = client.models.generate_content(
            model="lyria-3-pro-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO", "TEXT"],
                safety_settings=[ # 안전 필터 완화 (Lofi 음악 생성을 위해)
                    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
                ]
            ),
        )
        
        if response is None:
            raise Exception("Lyria API로부터 None 응답을 받았습니다.")

        audio_data = None
        
        # 1. response.parts 확인 (가장 일반적인 구조)
        if hasattr(response, 'parts') and response.parts:
            for part in response.parts:
                if part.inline_data is not None:
                    audio_data = part.inline_data.data
                    break
                elif hasattr(part, 'audio') and part.audio: # [보강] audio 속성 확인
                    audio_data = part.audio.data
                    break
        
        # 2. candidates 확인 (폴백 구조)
        if not audio_data and hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            # 안전 차단 여부 확인
            if candidate.finish_reason and candidate.finish_reason != "STOP":
                print(f"[Warning] Lyria 생성 중단됨. 원인: {candidate.finish_reason}")
                
            parts = getattr(candidate.content, 'parts', [])
            for part in parts:
                if part.inline_data is not None:
                    audio_data = part.inline_data.data
                    break
                elif hasattr(part, 'audio') and part.audio:
                    audio_data = part.audio.data
                    break
                
        if audio_data:
            os.makedirs(os.path.dirname(music_path), exist_ok=True)
            with open(music_path, "wb") as f:
                f.write(audio_data)
            print(f"[Agent Leo] Lyria 3 음악 생성 및 다운로드 성공: {music_path}")
            return music_path, music_prompt
        else:
            # 응답은 왔지만 데이터가 없는 경우의 디버깅 정보
            print(f"[Debug] Lyria 응답 분석 실패. 응답 요약: {response}")
            raise Exception("API 응답에서 오디오 데이터를 찾지 못했습니다.")
            
    except Exception as e:
        print(f"[Error] Lyria 3 음악 생성 실패: {e}")
        # 폴백 로직: 기존 음원 파일이 있다면 그것을 반환
        # (Cloud Run 환경에서는 도커 이미지에 내장된 기본 파일을 찾습니다)
        fallback_audio = "assets/branding/Neon_Blossom_Fallback_Lofi.mp3"
        if os.path.exists(music_path):
            print(f"[Agent Leo] 🚨 폴백 모드: 기존 캐시된 음원을 재사용합니다. ({music_path})")
            return music_path, music_prompt
        elif os.path.exists(fallback_audio):
            print(f"[Agent Leo] 🚨 폴백 모드: 기본 내장 음원을 사용합니다. ({fallback_audio})")
            return fallback_audio, music_prompt
        else:
            print("[Agent Leo] 🚨 폴백 실패: 로컬에서도 음원을 찾을 수 없습니다.")
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
        "Return ONLY a valid JSON object with keys: 'title', 'description', 'tags', and 'pinned_comment'. "
        "The description must read like a tender, poetic moment from the girl's day — personal and warm, NEVER corporate or AI-sounding. "
        "Title: 50-70 characters, emotionally resonant English. Use an em dash (—) for style. "
        "Pinned Comment: A warm, engaging question or thought to encourage listeners to share their current activity or memories, including subtle SEO keywords."
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
        f"3. TAGS: 20 high-traffic English YouTube tags as a JSON array.\n"
        f"4. PINNED_COMMENT: A warm, first-person question directed to the listeners to spark a conversation. "
        f"Make it deeply connected to the today's mood (e.g., studying, rainy nights, nostalgic memories)."
    )

    
    try:
        response = client.models.generate_content(
            model="gemini-3.1-pro-preview",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json"
            )
        )
        
        metadata_json = json.loads(response.text)
        
        # 글로벌(미국/유럽) 로파이 피크 타임 타겟팅
        # KST 12:00 (낮) = UTC 03:00 = EST 22:00 (미국 동부 밤 10시)
        from datetime import datetime, timedelta
        now = datetime.now()
        publish_time = now.replace(hour=12, minute=0, second=0, microsecond=0)
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
        # 폴백 시에도 글로벌 타겟 시간(KST 12:00/EST 10:00 PM) 동일 적용
        publish_time = now.replace(hour=12, minute=0, second=0, microsecond=0)
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
            "pinned_comment": "Thank you for stopping by. ✨ What are you studying or dreaming of today while listening to these jazzy lofi beats? I'd love to hear your story below.",
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
    
    # 0. 오늘의 '일상 순간' 선택 (Midnight Edition 시나리오)
    selected_scene = random.choice(LIFESTYLE_SCENES)
    visual_prompt = f"{ART_STYLE} {CHARACTER_DESCRIPTION} {selected_scene['subject']}. Lighting: {selected_scene['lighting']}. Mood: {selected_scene['mood']}."
    scene_mood = selected_scene['mood']
    
    # 1. 시도 순서: fal.ai (Grok) -> Nano Banana (Gemini) -> Fallback
    image_path, image_url = generate_fal_image(visual_prompt)
    
    if not image_path:
        print("[Agent Leo] fal.ai 스킵 또는 실패. Gemini Nano Banana로 전환합니다...")
        image_path, visual_prompt, scene_mood = generate_nano_banana_image(visual_prompt, scene_mood)
        image_url = None

    # 📺 [VFX] 빈티지 레트로 필터 적용 (80년대 감성 입히기)
    image_path = apply_vintage_vfx(image_path)
    
    # 2. Lyria 3를 통한 이미지 기반 음악 작곡 (멀티모달 감성 동기화)
    generated_audio_path, music_prompt = generate_lyria_music(image_path=image_path)
    if not generated_audio_path or not os.path.exists(generated_audio_path):
        print("🚨 [Agent Leo] Lyria 3 음악 생성 실패! 파이프라인을 중단합니다.")
        print("   → API 할당량 또는 네트워크 상태를 확인해주세요.")
        sys.exit(1)
    
    audio_path = generated_audio_path
    print("✅ [Agent Leo] Lyria 3 멀티모달 음악 생성 완료. 이미지의 무드가 사운드에 반영되었습니다.")
    
    if not os.path.exists(image_path):
        print(f"[Error] {image_path} 배너 이미지가 없습니다.")
        sys.exit(1)

    # 1.5. (선택 사항) 비디오 애니메이션 렌더링
    # 우선 순위: Grok Video (fal.ai) -> Veo 3 (Gemini) -> Static
    veo_path = None
    
    # [Agent Leo] Grok Video 시도 (Reference-to-Video)
    if image_url:
        veo_path = generate_fal_video(image_url, visual_prompt)
        
    # Grok Video 실패 시 Veo 3로 폴백
    if not veo_path:
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
        
        # [Agent Leo] 16:9 와이드 해상도 고정 (1920x1080)
        final_video = video.resize(newsize=(1920, 1080))
        
        final_video.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )
        print(f"✅ [Agent Leo] V5-Pro-SEO 와이드 합성 종료! 저장 경로: {output_path}")
    except Exception as e:
        print("[Error] 렌더링 도중 에러가 발생했습니다:", e)
        sys.exit(1)

if __name__ == "__main__":
    generate_video()

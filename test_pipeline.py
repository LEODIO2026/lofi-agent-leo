"""
로컬 파이프라인 테스트 — 이미지 + 음악 + 영상 파일 생성만 실행.
YouTube 업로드 없음.
"""
import os
import sys
import subprocess

# .env 로드
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

if not os.path.exists("credentials.json"):
    print("[Error] credentials.json 파일이 없습니다.")
    sys.exit(1)

if os.path.exists("token_full.json") and not os.path.exists("token.json"):
    import shutil
    shutil.copy("token_full.json", "token.json")

import random
import asset_generator as ag

def main():
    print("=" * 60)
    print(" [Test] 전체 파이프라인 테스트 (업로드 제외)")
    print("=" * 60)

    selected_scene = random.choice(ag.LIFESTYLE_SCENES)
    visual_prompt = (
        f"{ag.ART_STYLE} {ag.CHARACTER_DESCRIPTION} "
        f"Scene: {selected_scene['subject']}. "
        f"Composition: {selected_scene['shot_type']}. "
        f"Lighting: {selected_scene['lighting']}. "
        f"Mood: {selected_scene['mood']}."
    )
    scene_mood = selected_scene['mood']

    print(f"\n씬: {selected_scene['subject'][:80]}")
    print(f"무드: {scene_mood}\n")

    # ── Step 1: 이미지 생성 ──────────────────────────────
    print("─" * 40)
    print("[Step 1] 이미지 생성")
    print("─" * 40)
    image_path, visual_prompt, scene_mood = ag.generate_nano_banana_image(visual_prompt, scene_mood)
    if not image_path or not os.path.exists(image_path):
        print("[Test] Gemini 실패 → Kie.ai 폴백")
        image_path, _ = ag.generate_kie_image(visual_prompt)

    if not image_path or not os.path.exists(image_path):
        print("[Error] 이미지 생성 실패. 종료.")
        sys.exit(1)

    image_path = ag.apply_vintage_vfx(image_path)
    print(f"✅ 이미지: {image_path}")
    subprocess.run(["open", image_path])

    # ── Step 2: 음악 생성 ──────────────────────────────
    print("\n" + "─" * 40)
    print("[Step 2] 음악 생성 (Lyria 3)")
    print("─" * 40)
    audio_path, music_prompt = ag.generate_lyria_music(image_path=image_path)
    if not audio_path or not os.path.exists(audio_path):
        print("[Error] 음악 생성 실패. 종료.")
        sys.exit(1)

    print(f"✅ 음악: {audio_path}")
    subprocess.run(["open", audio_path])

    # ── Step 3: 영상 합성 ──────────────────────────────
    print("\n" + "─" * 40)
    print("[Step 3] 영상 합성 (FFmpeg)")
    print("─" * 40)
    output_path = "assets/test_output.mp4"
    # ffmpeg 경로 탐색 (시스템 PATH → /tmp 다운로드본 순)
    ffmpeg_bin = "ffmpeg"
    for candidate in ["/usr/local/bin/ffmpeg", "/opt/homebrew/bin/ffmpeg", "/tmp/ffmpeg"]:
        if os.path.isfile(candidate):
            ffmpeg_bin = candidate
            break

    zoom_expr = "1+0.025*sin(2*PI*on/(24*20))"
    cmd = [
        ffmpeg_bin, "-y",
        "-loop", "1", "-i", image_path,
        "-stream_loop", "-1", "-i", audio_path,
        "-t", "60",  # 테스트용 1분
        "-vf", (
            f"scale=1920:1080:force_original_aspect_ratio=increase,"
            f"crop=1920:1080,"
            f"zoompan=z='{zoom_expr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=24"
        ),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        print(f"[Error] FFmpeg 실패:\n{result.stderr[-1000:]}")
        sys.exit(1)

    print(f"✅ 영상: {output_path}")
    subprocess.run(["open", output_path])

    print("\n" + "=" * 60)
    print("✅ 테스트 완료! 파일 경로:")
    print(f"  이미지: {image_path}")
    print(f"  음악:   {audio_path}")
    print(f"  영상:   {output_path}")
    print("=" * 60)
    print("\n문제 없으면 Cloud Run에서 전체 파이프라인(10분 영상 + 업로드)이 실행됩니다.")

if __name__ == "__main__":
    main()

"""
이미지 생성 테스트 스크립트 — 이미지만 생성하고 저장 후 미리보기
음악 생성, 영상 합성, 유튜브 업로드는 수행하지 않습니다.
"""
import os
import sys
import subprocess

# .env 파일에서 API 키 로드 (로컬 테스트용, python-dotenv 불필요)
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

# 로컬에서 credentials.json 존재 확인
if not os.path.exists("credentials.json"):
    print("[Error] credentials.json 파일이 없습니다.")
    sys.exit(1)

# token_full.json → token.json 복사 (업로더 호환)
if os.path.exists("token_full.json") and not os.path.exists("token.json"):
    import shutil
    shutil.copy("token_full.json", "token.json")

import random
import asset_generator as ag

def main():
    print("=" * 60)
    print(" [Test] 이미지 생성 단독 테스트")
    print("=" * 60)

    # 오늘의 씬 선택
    selected_scene = random.choice(ag.LIFESTYLE_SCENES)
    visual_prompt = (
        f"{ag.ART_STYLE} {ag.CHARACTER_DESCRIPTION} "
        f"Scene: {selected_scene['subject']}. "
        f"Composition: {selected_scene['shot_type']}. "
        f"Lighting: {selected_scene['lighting']}. "
        f"Mood: {selected_scene['mood']}."
    )

    print(f"\n선택된 씬: {selected_scene['subject'][:80]}...")
    print(f"무드: {selected_scene['mood']}\n")

    # 1차: Kie.ai
    image_path, image_url = ag.generate_kie_image(visual_prompt)

    # 2차: Gemini 폴백
    if not image_path:
        print("[Test] Kie.ai 실패 → Gemini 폴백")
        image_path, visual_prompt, _ = ag.generate_nano_banana_image(visual_prompt, selected_scene['mood'])

    if not image_path or not os.path.exists(image_path):
        print("[Test] 이미지 생성 실패.")
        sys.exit(1)

    # VFX 필터 적용
    image_path = ag.apply_vintage_vfx(image_path)

    print(f"\n✅ 이미지 생성 완료: {image_path}")
    print("   미리보기를 열겠습니다. 확인 후 터미널로 돌아와 계속 진행하세요.\n")

    # macOS 기본 뷰어로 미리보기
    subprocess.run(["open", image_path])

    answer = input("이 이미지로 계속 진행하시겠습니까? (y/n): ").strip().lower()
    if answer != "y":
        print("취소됨. 다시 실행하여 새 이미지를 생성하세요.")
        sys.exit(0)

    print("\n✅ 이미지 컨펌. 실제 파이프라인(음악+영상+업로드)은 Cloud Run에서 실행됩니다.")
    print("   main_cloud.py를 로컬에서 실행하거나 Cloud Run Job을 수동 트리거하세요.")

if __name__ == "__main__":
    main()

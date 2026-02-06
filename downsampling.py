import os
import glob
import subprocess
import re

# ================= 설정 구역 =================
# 1번 경로: 인풋 소스 (RAW YUV 파일 원본)
INPUT_DIR = r"E:\Research\DatasetComp (김동휘님, 02.02~06)\RAW_YUV"

# 2번 경로: 아웃풋 소스 (다운샘플링된 YUV 저장소)
OUTPUT_DIR = r"E:\Research\DatasetComp (김동휘님, 02.02~06)\YUV_Downsampled"

# FFmpeg 실행 파일 경로 (환경 변수에 등록되어 있다면 "ffmpeg"만 써도 됩니다)
# 기존 스크립트와 경로를 통일하여 안정성을 높였습니다.
FFMPEG_PATH = r"D:\ffmpeg-2026-02-02-git-7e9fe341df-full_build\bin\ffmpeg.exe"

# =============================================

def downsample_yuv():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"폴더 생성됨: {OUTPUT_DIR}")

    # .yuv 파일 목록 가져오기
    yuv_files = glob.glob(os.path.join(INPUT_DIR, "*.yuv"))
    
    if not yuv_files:
        print(f"파일을 찾을 수 없습니다: {INPUT_DIR}")
        return

    # 파일명에서 해상도를 찾기 위한 패턴 (예: ..._2704x2028_...)
    res_pattern = re.compile(r"(\d+)x(\d+)")

    print(f"총 {len(yuv_files)}개의 파일을 처리합니다.")

    for input_path in yuv_files:
        filename = os.path.basename(input_path)
        
        # 파일명에서 원본 해상도 추출
        match = res_pattern.search(filename)
        if not match:
            print(f"[Skip] 해상도 정보가 파일명에 없습니다: {filename}")
            continue
            
        in_w, in_h = map(int, match.groups())
        
        # 1/2 다운샘플링 해상도 계산 (정수형)
        out_w, out_h = in_w // 2, in_h // 2
        
        # 출력 파일명 생성 (파일명의 원본 해상도 문자열을 출력 해상도로 치환)
        new_filename = filename.replace(f"{in_w}x{in_h}", f"{out_w}x{out_h}")
        output_path = os.path.join(OUTPUT_DIR, new_filename)

        # FFmpeg 명령어 구성 (bicubic 필터 사용)
        cmd = [
            FFMPEG_PATH,
            "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{in_w}x{in_h}",
            "-pix_fmt", "yuv420p",
            "-i", input_path,
            "-vf", f"scale={out_w}:{out_h}:flags=bicubic",
            "-f", "rawvideo",
            "-pix_fmt", "yuv420p",
            output_path
        ]

        print(f"\n[처리 중] {filename}")
        print(f" >> 해상도 변경: {in_w}x{in_h} -> {out_w}x{out_h}")
        
        try:
            # 변환 실행
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print(f" [완료] 저장 위치: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f" [에러] {filename} 변환 실패: {e.stderr.decode()}")

    print("\n" + "="*50)
    print("모든 다운샘플링 작업이 완료되었습니다.")
    print("="*50)

if __name__ == "__main__":
    downsample_yuv()
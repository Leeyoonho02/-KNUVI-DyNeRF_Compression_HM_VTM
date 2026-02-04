import os
import subprocess
import json
import glob

# ================= 설정 구역 =================
# FFmpeg 및 FFprobe 실행 파일 이름 (환경 변수에 등록되어 있어야 함)
FFMPEG = r"D:\ffmpeg-2026-02-02-git-7e9fe341df-full_build\bin\ffmpeg.exe"
FFPROBE = r"D:\ffmpeg-2026-02-02-git-7e9fe341df-full_build\bin\ffprobe.exe"

# 입력 데이터셋 폴더 (DyNeRF Dataset 폴더)
DATASET_DIR = r"./DyNeRF"

# 결과물이 저장될 YUV 폴더
# OUTPUT_DIR = r"./RAW_YUV"
OUTPUT_DIR = r"E:\Research\DatasetComp (김동휘님, 02.02~06)\yuv_new"

# ============================================

def get_video_info(file_path):
    """
    ffprobe를 사용하여 비디오의 너비, 높이, 프레임 수를 추출합니다.
    """
    cmd = [
        FFPROBE,
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,nb_frames",
        "-of", "json",
        file_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = json.loads(result.stdout)
        stream = info['streams'][0]
        width = stream['width']
        height = stream['height']
        frames = stream.get('nb_frames', 'unknown')
        
        # nb_frames가 없는 경우(일부 포맷) 전체 프레임을 다시 계산
        if frames == 'unknown':
             cmd_frames = [
                 FFPROBE, "-v", "error", "-select_streams", "v:0",
                 "-count_packets", "-show_entries", "stream=nb_read_packets",
                 "-of", "csv=p=0", file_path
             ]
             frames = subprocess.check_output(cmd_frames, text=True).strip()
             
        return width, height, frames
    except Exception as e:
        print(f"Error getting info for {file_path}: {e}")
        return None, None, None

def convert_mp4_to_yuv():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

    # 모든 하위 폴더의 .mp4 파일 탐색
    mp4_files = glob.glob(os.path.join(DATASET_DIR, "**", "*.mp4"), recursive=True)
    
    if not mp4_files:
        print(f"No .mp4 files found in {DATASET_DIR}")
        return

    print(f"Found {len(mp4_files)} MP4 files. Starting conversion...")

    for mp4_path in mp4_files:
        # 경로 정보 분리
        folder_name = os.path.basename(os.path.dirname(mp4_path))
        file_name = os.path.splitext(os.path.basename(mp4_path))[0]
        
        print(f"\nProcessing: {folder_name}/{file_name}.mp4")
        
        # 비디오 정보 가져오기
        width, height, frames = get_video_info(mp4_path)
        if not width or not height:
            print(f"  [Skip] Could not get metadata for {mp4_path}")
            continue

        # 출력 파일명 규칙: {시퀀스}_{파일명}_{너비}x{높이}_{프레임수}.yuv
        output_filename = f"{folder_name}_{file_name}_{width}x{height}_{frames}.yuv"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        # FFmpeg 변환 명령어
        # -pix_fmt yuv420p: 8비트 YUV 4:2:0 포맷 강제
        cmd = [
            FFMPEG,
            "-y", # 덮어쓰기 허용
            "-i", mp4_path,
            "-pix_fmt", "yuv420p",
            output_path
        ]

        print(f"  Converting to: {output_filename}")
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print(f"  [Success] Saved to {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"  [Error] Failed to convert {file_name}: {e.stderr.decode()}")

if __name__ == "__main__":
    convert_mp4_to_yuv()

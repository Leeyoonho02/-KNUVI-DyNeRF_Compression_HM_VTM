import os
import glob
import subprocess
import re
import time
import concurrent.futures

# ================= 설정 구역 (경로를 환경에 맞게 수정하세요) =================

# HM 인코더 실행 파일 경로 (상대 경로 사용)
HM_ENC_PATH = os.path.join(os.getcwd(), "HM", "bin", "vs16", "msvc-19.29", "x86_64", "release", "TAppEncoder.exe")

# FFmpeg 경로 (MP4 변환용)
FFMPEG_PATH = r"D:\ffmpeg-2026-02-02-git-7e9fe341df-full_build\bin\ffmpeg.exe"

# 설정 파일 경로
CONFIG_PATH = os.path.join(os.getcwd(), "HM", "cfg", "encoder_intra_main.cfg")

# 입력 YUV 파일들이 있는 폴더
INPUT_DIR = r"D:\DyNeRF_Compression_HM_VTM\Input_to_compress"

# 결과물이 저장될 최상위 폴더
OUTPUT_BASE_DIR = os.path.join(os.getcwd(), "Compressed")

# 처리할 QP 리스트
QP_LIST = [22, 27, 32, 37, 42]

# 병렬 처리에 사용할 프로세스 수 (8코어 중 6개 권장)
MAX_WORKERS = 6

# ===========================================================================

def encode_task(task_info):
    """
    개별 인코딩 작업을 수행하는 함수 (병렬 처리용)
    """
    input_path, qp, name, width, height, frames = task_info
    
    # QP별 출력 폴더 생성
    output_dir = os.path.join(OUTPUT_BASE_DIR, f"HEVC_QP{qp}")
    os.makedirs(output_dir, exist_ok=True)
    
    filename = os.path.basename(input_path)
    base_name = os.path.splitext(filename)[0]
    
    bitstream_path = os.path.join(output_dir, f"{base_name}.hevc")
    recon_path = os.path.join(output_dir, f"{base_name}.yuv")
    log_path = os.path.join(output_dir, f"{base_name}_log.txt")
    mp4_path = os.path.join(output_dir, f"{base_name}.mp4")

    # 명령어 구성
    cmd = [
        HM_ENC_PATH,
        "-c", CONFIG_PATH,
        "-i", input_path,
        "-b", bitstream_path,
        "-o", recon_path,
        f"--SourceWidth={width}",
        f"--SourceHeight={height}",
        "-fr", "30",
        "--FrameSkip=0",
        f"--FramesToBeEncoded={frames}",
        "--InputBitDepth=8",
        "--InputChromaFormat=420",
        "--InternalBitDepth=8",
        f"--QP={qp}",
        "--ConformanceWindowMode=1"
    ]

    print(f"[Start] {filename} (QP {qp})")
    start_time = time.time()
    
    try:
        # 인코딩 실행
        with open(log_path, "w") as log_file:
            result = subprocess.run(cmd, stdout=log_file, stderr=subprocess.STDOUT, text=True)
        
        if result.returncode == 0:
            # MP4 변환
            mux_cmd = [FFMPEG_PATH, "-y", "-i", bitstream_path, "-c", "copy", mp4_path]
            subprocess.run(mux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            
            end_time = time.time()
            duration_min = (end_time - start_time) / 60
            print(f"[Done] {filename} (QP {qp}) - {duration_min:.2f} min")
            return True
        else:
            print(f"[Error] {filename} (QP {qp}) - Check {log_path}")
            return False
            
    except Exception as e:
        print(f"[Fatal] {filename} (QP {qp}): {str(e)}")
        return False

def run_parallel_encoding():
    yuv_files = glob.glob(os.path.join(INPUT_DIR, "*.yuv"))
    filename_pattern = re.compile(r"(.+)_(\d+)x(\d+)_(\d+)\.yuv")

    if not yuv_files:
        print(f"경고: {INPUT_DIR} 경로에서 .yuv 파일을 찾을 수 없습니다.")
        return

    # 작업 리스트 생성
    tasks = []
    for qp in QP_LIST:
        for input_path in yuv_files:
            match = filename_pattern.match(os.path.basename(input_path))
            if match:
                name, width, height, frames = match.groups()
                tasks.append((input_path, qp, name, width, height, frames))

    print(f"총 {len(tasks)}개의 인코딩 작업을 {MAX_WORKERS}개의 코어로 병렬 시작합니다.")
    
    start_all = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(encode_task, tasks)
    
    end_all = time.time()
    print(f"\n모든 작업 완료! 전체 소요 시간: {(end_all - start_all)/60:.2f} min")

if __name__ == "__main__":
    run_parallel_encoding()
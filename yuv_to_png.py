import os
import glob
import subprocess
import re

# ================= 설정 구역 =================

# FFmpeg 실행 파일 경로 (환경 변수에 등록되어 있다면 "ffmpeg"만 써도 됨)
FFMPEG_PATH = "ffmpeg" 

# YUV 파일이 들어있는 최상위 폴더 (인코딩 결과물이 저장된 곳)
WORK_DIR = os.path.join(os.getcwd(), "Compressed")

# 처리할 QP 리스트 (폴더명 탐색용)
QP_LIST = [22, 27, 32, 37, 42]

# YUV 픽셀 포맷 (이전 인코딩 설정이 8비트 4:2:0 이었으므로 yuv420p)
# 만약 10비트로 인코딩했다면 'yuv420p10le'로 변경해야 함
PIX_FMT = "yuv420p"

# ============================================

def yuv_to_png():
    # 해상도 파싱을 위한 정규표현식 (파일명 중간의 숫자x숫자 패턴을 찾음)
    # 예: flower_1008x756_34_rec.yuv -> 1008, 756 추출
    res_pattern = re.compile(r"(\d+)x(\d+)")

    for qp in QP_LIST:
        # QP별 폴더 경로 (예: ...\HEVC_QP22)
        current_dir = os.path.join(WORK_DIR, f"VVC_QP{qp}")
        #current_dir = os.path.join(r"D:\ECCV_2026\Dataset\LLFF\Compressed\YUV")
        
        if not os.path.exists(current_dir):
            print(f"[Skip] 폴더 없음: {current_dir}")
            continue

        # 해당 폴더 내의 모든 .yuv 파일 찾기
        yuv_files = glob.glob(os.path.join(current_dir, "*.yuv"))
        
        print(f"\n>>> Processing QP: {qp} ({len(yuv_files)} files found)")

        for input_yuv in yuv_files:
            filename = os.path.basename(input_yuv)
            
            # 해상도 추출
            match = res_pattern.search(filename)
            if not match:
                print(f"[Skip] 해상도 정보 없음: {filename}")
                continue
            
            width, height = match.groups()
            
            # 파일명 베이스 (확장자 제거)
            base_name = os.path.splitext(filename)[0]
            
            # PNG 저장할 폴더 생성 (파일 하나당 폴더 하나 생성하여 정리)
            # 예: ...\VVC_QP22\PNG\flower_1008x756_34_rec\
            output_png_dir = os.path.join(current_dir, "PNG", base_name)
            os.makedirs(output_png_dir, exist_ok=True)
            
            # 출력 파일 패턴 (image_001.png, image_002.png ...)
            output_pattern = os.path.join(output_png_dir, "frame_%04d.png")

            # FFmpeg 명령어 구성
            # -f rawvideo: 헤더 없는 raw 파일임을 명시
            # -vcodec rawvideo: 비디오 코덱 raw
            # -s: 해상도 지정 (필수)
            # -pix_fmt: 픽셀 포맷 지정 (필수, 안 맞으면 색이 깨짐)
            # -i: 입력 파일
            cmd = [
                FFMPEG_PATH,
                "-y",                  # 덮어쓰기 허용
                "-f", "rawvideo",
                "-vcodec", "rawvideo",
                "-s", f"{width}x{height}",
                "-pix_fmt", PIX_FMT,
                "-r", "30",            # 프레임레이트 (PNG 추출엔 큰 영향 없으나 설정 권장)
                "-i", input_yuv,
                output_pattern
            ]

            print(f"Extracting: {filename} -> {output_png_dir}")
            
            # 명령어 실행 (로그는 생략하거나 필요시 캡처)
            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                print(f"  [Error] FFmpeg failed for {filename}")
                print(result.stderr) # 에러 발생 시에만 FFmpeg 로그 출력

if __name__ == "__main__":
    yuv_to_png()
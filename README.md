# [KNUVI] Dataset Compression Project

이 프로젝트는 지정된 데이터셋(DyNeRF)을 HEVC(HM) 및 VVC(VTM) 코덱을 사용하여 다양한 QP(Quantization Parameter) 설정값으로 압축하고 분석하기 위한 환경입니다.

## 📅 프로젝트 기간
- **수행 기간**: 2026.02.02 ~ 2026.02.06
- **주요 목표**: 다양한 인코딩 설정에 따른 압축 성능 분석 및 결과물 제출

---

## 📂 디렉토리 구조

```text
.
├── DyNeRF/                 # 원본 데이터셋 (시퀀스별 .mp4 파일 포함)
├── HM/                     # HEVC Reference Software (HM 16.20 등)
├── VVCSoftware_VTM/        # VTM Reference Software (VTM 11.0 등)
├── RAW_YUV/                # MP4에서 변환된 RAW YUV 파일 저장소
├── Compressed/             # QP별 최종 압축 결과물 (.hevc, .vvc, .yuv)
├── mp4_to_yuv.py           # MP4 -> YUV 변환 스크립트
├── HM_encoding.py          # HEVC(HM) 일괄 인코딩 스크립트
├── VTM_encoding.py         # VVC(VTM) 일괄 인코딩 스크립트
├── yuv_to_png.py           # YUV -> PNG 변환 (결과 확인용)
├── todolist.md             # 작업 할당 및 요구 사항 정리
└── log.md                  # 작업 진행 로그
```

---

## 🚀 사용법

모든 스크립트는 프로젝트 루트 디렉토리에서 실행하는 것을 권장합니다.

### 1. 환경 준비
`FFmpeg` 및 `FFprobe`가 시스템에 설치되어 있어야 합니다. `mp4_to_yuv.py` 내의 실행 파일 경로(`FFMPEG`, `FFPROBE`)가 본인의 환경에 맞는지 확인하세요.

### 2. MP4를 YUV로 변환
코덱(HM, VTM)은 RAW YUV 포맷만 입력으로 지원합니다.
```bash
python mp4_to_yuv.py
```
- `DyNeRF` 폴더 내의 `.mp4` 파일을 찾아 `RAW_YUV` 폴더에 `{시퀀스}_{파일명}_{너비}x{높이}_{프레임수}.yuv` 형식으로 변환합니다.

### 3. HEVC (HM) 인코딩 실행
```bash
python HM_encoding.py
```
- `QP_LIST = [22, 27, 32, 37, 42]` 설정에 따라 `All Intra` 모드로 인코딩을 진행합니다.
- 결과는 `Compressed/HEVC_QP{NN}/` 폴더에 저장됩니다.

### 4. VVC (VTM) 인코딩 실행
```bash
python VTM_encoding.py
```
- VVC 표준에 따른 압축을 진행합니다.
- 결과는 `Compressed/VVC_QP{NN}/` 폴더에 저장됩니다.

---

## ⚙️ 주요 설정 및 기술 요구 사항

- **사용 모드**: All Intra Mode (모든 프레임을 I-프레임으로 압축)
- **필수 QP**: 22, 27, 32, 37, 42
- **프레임 레이트**: 기본 30 fps (스크립트 내에서 수정 가능)
- **컬러 포맷**: YUV 4:2:0 (8-bit)

---

## 📦 최종 제출 결과물
- **원본 데이터**: `.mp4` 및 변환된 `.yuv`
- **압축 데이터**: 각 QP별 생성된 비트스트림(`.hevc`, `.vvc`) 및 복원된 `.yuv`
- **로그**: 인코딩 과정에서 생성된 각 파일별 `_log.txt`

---
*문의 사항은 `todolist.md` 또는 `log.md`를 참고하시기 바랍니다.*

## 1. 프로젝트 개요

* 
**프로젝트명**: [KNUVI] Dataset Compression 


* 
**수행 기간**: 2026.02.02 ~ 2026.02.06 


* 
**주요 목표**: 지정된 데이터셋을 HEVC 및 VVC 코덱을 사용하여 다양한 QP 설정값으로 압축 및 분석 



---

## 2. 작업 대상 데이터셋 (DyNeRF)

다음의 6개 시퀀스를 대상으로 작업을 진행해야 합니다. 

* coffee_martini 


* cook_spinach 


* cut_roasted_beef 


* flame_salmon_1 (4개의 파일로 분할됨) 


* flame_steak 


* sear_steak 



---

## 3. 기술적 요구 사항 및 인코딩 설정

### 사전 준비 (포맷 변환)

* 사용되는 코덱(VTM, HM)은 **YUV 형식만 입력으로 지원**합니다. 


* 따라서 기존의 `.mp4` 파일들을 `ffmpeg` 등을 이용하여 `.yuv`로 먼저 변환해야 합니다. 



### 사용 코덱 및 모드

* 
**코덱**: HEVC (HM), VVC (VTM) 


* 
**설정 모드**: All Intra Mode 


* 
**VTM 설정 파일**: `./VVCSoftware_VTM/cfg/encoder_intra_vtm.cfg` 


* 
**HM 설정 파일**: `./HM/cfg/encoder_intra_main.cfg` 





### 양자화 파라미터 (QP) 옵션

* 
**필수 QP**: 22, 27, 32, 37, 42 


* 상황에 따라 57까지의 범위 내에서 추가 옵션을 사용할 수 있습니다. 



---

## 4. 최종 제출 결과물

작업 완료 후 다음 파일들을 정리하여 제출해야 합니다. 

* 
**압축 전(Uncompressed) 데이터**: 원본 `.yuv` 파일 및 `.mp4` 파일 


* 
**압축 후(Compressed) 데이터**: 각 QP별(22, 27, 32, 37, 42) 결과물 


* 생성된 `.yuv` 파일 


* 생성된 `.mp4` 파일 


* 인코딩 로그 파일 
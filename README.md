# 🏗️ Dacon 구조물 안정성 예측 프로젝트

이 프로젝트는 구조물 이미지에서 배경과 노이즈를 제거하고, 객체의 구조적 특징을 극대화하여 적재 상태의 안정성(Stable/Unstable)을 정밀하게 예측하는 파이프라인을 구축하는 것을 목표로 합니다.

## 📂 파일별 상세 설명

### 1. `data_segmentation.ipynb` (Segmentation Research & Pipeline)
* **목적**: 최적의 세그멘테이션 기법을 탐색하여 정교한 객체 마스크 생성.
* **주요 실험 내용**:
    * **SAM 2 + 전처리 필터**: Gamma Boost, Shadow Masking 등을 통한 조명 변화 대응 실험.
    * **Depth-Anything-v2**: 깊이 정보를 활용한 객체 분리 기법 테스트.
    * **HSV + SAM 2 Hybrid (최종 채택)**: 
        * HSV 색공간 분석을 통해 물체의 위치(Smart Box)를 동적으로 파악.
        * 탐지된 영역을 SAM 2의 프롬프트로 입력하여 배경과 그림자가 완벽히 제거된 마스크 획득.
* **결론**: **HSV 스마트 박스 기반의 SAM 2 하이브리드 방식**이 가장 우수한 성능을 보여 최종 전처리 공정으로 결정.

### 2. `data_split.py`
* **목적**: 데이터셋 경로 관리 및 학습/검증 데이터 분리 자동화 스크립트.

### 3. `5_fold.ipynb` (Baseline Pipeline)
* **목적**: 생성된 마스크를 활용한 4채널 기반의 안정성 예측 모델 베이스라인 구축.
* **핵심 기능**:
    * RGB(3ch) + Mask(1ch)를 결합한 4채널 입력 구조.
    * Front/Top 뷰의 특징을 결합하는 `UltimateFusionNet` 설계.
    * Train + Dev 데이터 통합 및 Stratified 5-Fold 교차 검증 적용.

### 4. `5_fold_v2.ipynb`
* **목적**: 고해상도 이미지와 대형 백본 모델을 통한 성능 극대화.
* **주요 사양**:
    * **384x384** 고해상도 입력으로 미세한 구조적 특징 포착.
    * **ConvNeXt-Base** (384px 사전 학습 버전) 백본 사용.
    * 내부 검증(Val LogLoss) **0.0006** 대 달성.

## 🚀 주요 전략 및 결론
* **Hybrid Segmentation**: 단순 모델 사용이 아닌 HSV 색상 분석과 SAM 2를 결합하여 전처리 정확도를 비약적으로 향상.
* **Data Integration**: `dev` 데이터를 학습에 포함하고 이중 층화 추출을 적용하여 모델의 일반화 성능 확보.
* **Resolution Scaling**: 224px에서 384px로의 상향이 구조물 안정성 판단에 결정적인 역할을 함을 확인.

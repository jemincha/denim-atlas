# Denim Atlas 오픈소스 활용 검토

확인일: 2026-10-26. 공식 저장소·모델 카드·문서를 확인한 기술 검토다. 기존에 쓰던 OpenCLIP/Marqo 외의 후보는 설치하거나 실행하지 않았다. 아래 도입 판단은 현재 데이터 규모, 단일 평가자 라벨, Kaggle GPU와 구형 로컬 랩탑 조건에 대한 프로젝트 판단이다.

## 결론

현재 OpenCLIP + Marqo-FashionSigLIP을 유지한다. 다음 우선순위는 다른 모델을 더 얹는 것이 아니라 같은 입력·후보·라벨로 B0/B1을 비교하고 실패 원인을 확인하는 것이다. 바지 영역 분리가 실제 병목이면 SAM 2를 작은 별도 실험으로 검토한다. 파인튜닝은 같은 상품 분류가 아니라 **동일 query 안에서 더 비슷하다고 판정된 후보를 덜 비슷한 후보보다 가깝게 만드는 학습**으로 설계한다. 현재 3개 query로 학습·최종 평가를 동시에 하지 않는다.

## 후보별 활용

| 후보 / 공식 출처 | 실제 기능·라이선스 | Denim Atlas 활용안 | 현재 결정 |
|---|---|---|---|
| [OpenCLIP](https://github.com/mlfoundations/open_clip), [라이선스](https://github.com/mlfoundations/open_clip/blob/main/LICENSE) | CLIP/SigLIP 로딩·전처리·학습 구현, MIT | 이미 검증한 3.3.0으로 특징 추출. 향후 이미지 encoder의 제한된 파인튜닝에 사용 | **계속 사용**. 최신 main의 추가 기능을 3.3.0에 있다고 가정하거나 비교 중 업그레이드하지 않음 |
| [Marqo-FashionCLIP 저장소](https://github.com/marqo-ai/marqo-FashionCLIP), [FashionSigLIP 모델 카드](https://huggingface.co/Marqo/marqo-fashionSigLIP) | 패션 임베딩·공개 benchmark 평가 코드. 저장소/해당 모델 카드 Apache-2.0 | 기존 체크포인트·768차원 특징 유지. 공식 평가 구현은 재현성/대조 실험 참고 | **기존 모델 유지**. 공식 7개 데이터셋 결과는 우리 데님 유사도 성능이 아님 |
| [PyTorch Metric Learning](https://github.com/KevinMusgrave/pytorch-metric-learning), [명시적 pair/triplet 입력 문서](https://kevinmusgrave.github.io/pytorch-metric-learning/losses/) | Triplet/contrastive loss, mining, distance/reducer 모듈. MIT | query별 ordinal 판정으로 명시적 triplet 생성. 복잡한 miner가 필요해질 때 활용 | **조건부 후보**. 첫 단순 ranking loss는 기존 PyTorch로 충분하면 추가 설치하지 않음 |
| [SAM 2](https://github.com/facebookresearch/sam2) | 이미지/영상 promptable segmentation. 핵심 코드·가중치 Apache-2.0, 일부 제3자 구성 별도 고지 | 바지 box/point에서 mask 제안 → 검토 → 배경·상의 영향 비교 | **우선 검토할 전처리 후보**. 아직 도입·성능 향상 미확인. 설치 문서는 Python≥3.10, torch≥2.5.1 등을 요구하므로 Kaggle 별도 환경에서 확인 |
| [FiftyOne](https://github.com/voxel51/fiftyone), [유사도 문서](https://docs.voxel51.com/user_guide/similarity.html) | 데이터셋 시각 검토, 임베딩 유사도 검색·중복 후보 검토. 오픈소스 저장소 Apache-2.0 | 이미지/box/출처/그룹/판정과 실패 사례를 한 화면에서 검토 | **규모 확장 시 검토**. 현 27장에는 기존 정적 판정지와 JSON으로 충분. 외관이 비슷하다고 같은 상품으로 자동 병합하지 않음 |
| [FAISS](https://github.com/facebookresearch/faiss) | dense vector 검색·클러스터링, CPU/GPU 구현. MIT | 후보 수가 늘어 exact dot product가 병목일 때 정규화 임베딩 검색 가속 | **보류**. 현재 24개 후보에는 불필요. 검색 속도를 개선하는 도구이며 임베딩 품질을 학습하는 모델이 아님 |

## 그대로 가져오면 생기는 오류

Metric Learning 기본 예제는 같은 클래스 라벨끼리 positive를 만든다. 우리 목표에서는 제품 A와 B가 달라도 비슷할 수 있고, 같은 제품도 워싱·조명에 따라 달라 보일 수 있다. 특히 pair별 유사도는 전이적 클래스가 아니다. 사용자 0~3점을 전역 클래스 ID로 넣거나 상품 ID를 정답으로 넣지 않는다. 명시적 query-positive-negative 관계만 학습용 split 안에서 구성한다. [기본 예제](https://github.com/KevinMusgrave/pytorch-metric-learning#using-losses-and-miners-in-your-training-loop)와 [indices_tuple 문서](https://kevinmusgrave.github.io/pytorch-metric-learning/losses/)에서 이 차이를 확인했다.

OpenCLIP의 기본 CLIP/SigLIP loss와 이미지-텍스트 학습 CLI도 이미지 간 ordinal 판정 과제를 자동으로 해결하지 않는다. 모델 로딩·전처리는 재사용하고 연구 목적에 맞는 supervision을 별도로 구성한다. [3.3.0 loss 구현](https://github.com/mlfoundations/open_clip/blob/v3.3.0/src/open_clip/loss.py)을 확인했으며 아직 새 loss 실험은 하지 않았다.

SAM 2는 바지를 의미적으로 완벽하게 인식하는 자동 라벨러가 아니다. prompt와 mask 검토가 필요하다. 마스크가 바지 페이딩을 잘라내거나 다른 사람의 바지까지 포함하면 오히려 연구 입력이 틀어진다. 기존 사각 크롭 baseline을 보존한 채 분리된 ablation으로 측정한다. 기존 B1은 전체 크롭 평균 RGB이므로 mask 안의 색 통계로 바꿀 경우 다른 대조군으로 이름·전처리·체크섬을 기록한다.

근접 중복 검출 역시 원본 hash 검사를 대체하지 않는다. hash가 다른 파생 사진, 같은 제품의 여러 촬영, 단지 비슷한 다른 제품을 구분해야 한다. 임베딩 근접 결과는 검토 후보이며 제품 동일성의 증거로 자동 승격하지 않는다.

## 적용 순서와 통과 기준

1. **지금 준비한 예비 비교:** 동일 27개 크롭을 pinned encoder로 원격 추출하고, 고정 w=0.5의 B0/B1을 사용자 라벨과 비교. 불완전한 Q1에는 지표를 계산하지 않고 Q2/Q3 결과도 calibration으로 명시. 실제 결과가 저장돼야 실행 완료다.
2. **오류 기반 전처리 선택:** 배경/신발/상의가 주요 실패 원인으로 관찰되면 SAM 2 작은 표본 검토를 제안. mask 품질과 기존 크롭 대비 순위 변화를 함께 확인한 뒤 확대 여부를 판단한다.
3. **학습 자료 확장:** 충분한 서로 다른 query, 상품·파생사진 그룹 검토, train/validation/test 분리 후 추가 사람 판정. 무엇을 어떤 기준으로 더 판정할지 사용자가 볼 수 있는 묶음으로 준비한다.
4. **최소 파인튜닝:** 단순 이미지 ranking loss부터 검증. 복잡한 mining이 필요할 때만 PyTorch Metric Learning을 도입하고 버전 고정·gradient/재시작 검증을 수행한다. validation에서만 설정 선택, test는 마지막 비교에 사용한다.
5. **검색·관리 확장:** 속도/메모리 또는 검토 작업량이 실제 병목이 될 때 FAISS/FiftyOne을 도입한다. 그 전에는 추가 서버·벡터 DB·앱 UI를 만들지 않는다.

소프트웨어와 모델 라이선스는 이미지 데이터 이용 권한과 별개다. 위 저장소를 쓴다고 Pinterest/쇼핑몰 사진의 학습·배포 권한이 생기지는 않는다. 후보 설치, 새 모델 가중치 다운로드, 성능 개선을 이 검토만으로 완료했다고 주장하지 않는다.

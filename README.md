# bentoml_test_deploy

# 작동 방법
## Git LFS 가 필요합니다.
 - brew install git-lfs
 - git clone 한 repository 내에서  cd /bentoml_test_deploy
 - git lfs pull # lfs 로 저장된 파일 불러오기
## Dockfile 실행
 - docker build -t bento_test .
 - docker run -p 8000:3000 bento_test
## Test
 - 만약 결과를 포함해서 보고싶다면
   - python local_api_check.py
 - 결과와 관계없이 동작 여부 체크
   - pytest

# 세부 과정 설명
## 모델 구축
 - VIT 모델을 구축하기 위해 오픈소스인 vit_b16 모델을 기반으로 작성하였습니다.
 - 이때 데이터 증강기법으로는 ImageDataGenerator 을 활용하였고 학습 속도를 향상시키기 위해 GPU 를 활용하였습니다.
 - overfitting 방지를 위한 iamge resizing, normalization 등의 과정을 거치도록 구성하였습니다.
 - 하이퍼 파라미터 튜닝은 ReduceLROnPlateau,EarlyStopping 을 활용하여 진행하였습니다.
 - 단 Local 환경에서 리소스의 한계로 epochs 나 batch size 는 자유롭게 설정하며 개선시키지 못하였습니다.
 - 최종 정확도는 약 73% 를 얻을 수 있었습니다.

## 배포 과정
 - 배포는 bentoml 기반으로 이루어지며 이는 dockerfile 을 기준으로 작동 될 수 있도록 구성하였습니다.
 - dockerfile 내에서 model load 가 이루어지며 이때 기존에 훈련된 모델의 가중치와 구조를 재활용하는 형태로 구성하였습니다.
 - 또한 bentoml 에서 사용가능한 service 파일을 제작하여 이를 기반으로 API 가 배포될 수 있도록 제작하였습니다.
 - 이때 해당 API 가 정상작동 하는지에 대한 Test 를 진행할 수 있도록 pytest 파일을 추가해두었습니다. 

# 비고
- 모델 구축시 opensource 모델인 vit_b16 을 활용하였습니다. 해당 모델 내 tensorflow addons 로 인해 정상적으로 docker image build 가 불가능하여 dockfile 내에서는 해당 모델은 제거했습니다.
  - 시간이 부족하여 다시 모델을 만들어 정상적으로 작동시키지는 못했습니다.
- dockfile 을 제공하기위해 위와같이 제작하였지만 다양한 다른 방식도 있을것 같습니다.
  - 이전에 bentoml 을 잠시 다뤄본적있으나 시간이 부족하여 이전처럼 Monitoring 인프라 구축과 부하테스트를 진행하지 못했습니다.
  - 만약 구축하고자 하면 아래와 같이 할 수 있을것 같습니다.
    - 링크 : https://www.notion.so/onchaindatastudy/MLops-Kubernets-BentoML-24f081f685c347a0958d2effb5994ced

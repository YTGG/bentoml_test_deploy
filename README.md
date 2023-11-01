# bentoml_test_deploy

# 작동 방법
## Git LFS 가 필요합니다.
 - brew install git-lfs
 - git clone 위 repository
 - cd /bentoml_test_deploy
 - git lfs pull # lfs 로 저장된 파일 불러오기
## Dockfile 실행
 - docker build -t bento_test .
 - docker run -p 8000:3000 bento_test
## Test
 - 만약 결과를 포함해서 보고싶다면
   - python local_api_check.py
 - 결과와 관계없이 동작 여부 체크
   - pytest

# 비고
- 모델 구축시 opensource 모델인 vit_b16 을 활용하였습니다. 해당 모델 내 tensorflow addons 로 인해 정상적으로 docker image build 가 불가능하여 dockfile 내에서는 해당 모델은 제거했습니다.
  - 시간이 부족하여 다시 모델을 만들어 정상적으로 작동시키지는 못했습니다.
- dockfile 을 제공하기위해 위와같이 제작하였지만 다양한 다른 방식도 있을것 같습니다.
  - 이전에 bentoml 을 잠시 다뤄본적있으나 시간이 부족하여 이전처럼 Monitoring 인프라 구축과 부하테스트를 진행하지 못했습니다.
  - 만약 구축하고자 하면 아래와 같이 할 수 있을것 같습니다.
    - 링크 : https://www.notion.so/onchaindatastudy/MLops-Kubernets-BentoML-24f081f685c347a0958d2effb5994ced

# 1. Requirements
- python >= 3.8
- tensorflow 2.8.0
- scikit-learn 1.0.2
- pandas 2.0.3
- numpy 1.24.5
- pydantic 2.3.0
- pydantic-settings 2.0.3
- beanie 1.21.0
- tqdm 4.66.1
> install
> ~~~bash
> pip install -r requirements.txt
> ~~~

# 2. Description
> ## dev.env (KOR)
> ~~~ python
> # TimeGan Default Setting
> # 1 이나 2 설정하면 됩니다.
> DATA_TYPE=1
> # 초 S, 분 T
> FREQ=S
> 
> # 데이터베이스 세팅
> # 테스트를 하려면 DB_TEST를 True로 설정하시면 됩니다
> DB_TEST=True
> DB_URI=mongodb://127.0.0.1:27017/
> 
> # DB_TEST가 False시 설정합니다. 
> DB_USER=dev
> DB_PWD=dev123
> DB_HOST=127.0.0.1:27017
> DB_DATABASE=DataGenerated
> DB_COLLECTION=DataGenerated{GEN_TYPE}
> 
> # 경로를 설정합니다. 상대경로도 지원합니다.
> SCALE_PATH=./models/${GEN_TYPE}/scale.pkl
> MODEL_PATH=./models/${GEN_TYPE}/synthetic_data
> ~~~
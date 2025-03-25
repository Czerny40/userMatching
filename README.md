# 헬스 파트너 매칭 서비스

<div align="center">

![Honeycam 2025-03-25 15-51-45](https://github.com/user-attachments/assets/4a08c6e3-9a6b-4fa2-a873-c099e3ecee9d)

</div>

## 프로젝트 소개

해당 서비스는 FitConnect에서 사용자의 운동 능력과 위치를 기반으로 적합한 운동 파트너를 매칭해주는 서비스입니다. 시스템은 Spring Boot 기반의 메인 서버와 FastAPI 기반의 매칭 서버로 구성되어 있습니다. 사용자의 신체 정보, 운동 능력(벤치프레스, 스쿼트, 데드리프트), 위치 정보를 활용하여 적합한 운동 파트너를 추천합니다.

## 시작 가이드
### Requirements
For building and running the application you need:

- Python : 3.11.x
  
### Installation
```
git clone https://github.com/Czerny40/userMatching.git
cd userMatching
```
#### requirements
```
pip install -r requirements.txt
```
#### 환경 변수 설정
.env 파일 생성 후 KAKAO_API_KEY 등 필요한 환경 변수 설정

#### run
```
uvicorn main:app --reload
```

---
## 주요 기능 📦

### ⭐️ IPF GL 점수 기반 운동 능력 평가
### ⭐️ 위치 기반 매칭 (카카오 API 활용)
### ⭐️ 유사도 계산을 통한 최적의 파트너 매칭

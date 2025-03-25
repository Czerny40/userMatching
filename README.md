# 헬스 파트너 매칭 서비스

<div align="center">

![Honeycam 2025-03-25 15-51-45](https://github.com/user-attachments/assets/4a08c6e3-9a6b-4fa2-a873-c099e3ecee9d)

</div>

## 소개

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
## API Docs
API 엔드포인트에 대한 자세한 설명은 다음 URL에서 확인할 수 있습니다
- Swagger UI: http://서버주소:포트/docs
- ReDoc: http://서버주소:포트/redoc
---
## 주요 기능 📦

### ⭐️ IPF GL 점수 기반 운동 능력 평가
### ⭐️ 위치 기반 매칭 (카카오 API 활용)
### ⭐️ 유사도 계산을 통한 최적의 파트너 매칭
---

## 매칭 알고리즘 설명
### IPF GL 점수 계산 방식
IPF GL(International Powerlifting Federation Goodlift) 점수는 성별과 체중에 따른 상대적인 근력 수준을 평가하는 지표입니다.

- 계산 공식:

```
IPF GL 점수 = 100 * 총 중량 / (a - b * e^(-c * 체중))
```
- 성별에 따른 계수:

  - 남성(M): a = 1199.72839, b = 1025.18162, c = 0.00921
  
  - 여성(F): a = 610.32796, b = 1045.59282, c = 0.03048

- 총 중량 계산:

```
총 중량 = 벤치프레스 + 스쿼트 + 데드리프트
```
예시:
남성, 체중 80kg, 총 중량 430kg인 경우:

```
IPF GL 점수 = 100 * 430 / (1199.72839 - 1025.18162 * e^(-0.00921 * 80))
```
### 유사도 계산 방법 및 가중치
두 사용자 간의 유사도는 키 차이, 근력 차이, 성별 일치 여부를 고려하여 계산됩니다.
가중치는 사용자의 피드백을 통해 수정할 수 있습니다.

- 키 차이 계산:

```
height_diff = |사용자1.키 - 사용자2.키| / 50
```
- 근력 차이 계산:

```
strength_diff = |사용자1.IPF_GL점수 - 사용자2.IPF_GL점수| / 500
```
- 성별 페널티:

```
gender_penalty = 1 (성별이 다른 경우), 0 (성별이 같은 경우)
```
- 최종 유사도 계산:

```
유사도 = height_diff * 0.1 + strength_diff * 0.5 + gender_penalty * 0.1
```
- 가중치 설명:

  - 키 차이: 10% 가중치 (키 차이가 클수록 유사도 감소)
  
  - 근력 차이: 50% 가중치 (근력 차이가 클수록 유사도 감소)
  
  - 성별 일치: 10% 가중치 (성별이 다르면 유사도 감소)

### 거리 계산 방법
두 사용자 간의 물리적 거리는 위도와 경도를 사용한 Haversine 공식으로 계산됩니다.
KAKAO MAPS의 API를 통해 위도, 경도값을 구했습니다.

- Haversine 공식:

```
a = sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)
c = 2 * atan2(√a, √(1-a))
거리 = R * c (R은 지구 반지름 6371km)
```
- 매칭 조건:

  - 거리가 3km 이내인 사용자만 매칭 대상으로 고려됩니다.
  
  - 매칭된 사용자들은 유사도가 낮은 순으로 정렬됩니다(유사도가 낮을수록 더 적합한 매칭).
  
  - 한 페이지당 5명의 매칭 결과가 표시됩니다.

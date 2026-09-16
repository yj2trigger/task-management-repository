# al:ready Kaggle 챌린지 — 대회별 스펙 (Day1~Day5)

> 2026-09-16: Claude 프로젝트 메모리에 있던 대회 메모 5개를 여기로 옮겼다. 작업 규칙은 [`WORKING_RULES.md`](./WORKING_RULES.md).
> 주최: al:ready(제6대 인공지능학과 학생회) 여름방학 AI 챌린지, host 이나영(ERICA 인공지능학과).
> 공통 규칙: 하루 5회 제출 제한, 블로그 포스팅 필수(6항목), 순위 미기록 시 0점.
> 작업 폴더: `C:\onedrive\_대학교\kaggle 대회\day-0X\`

---

## Day1 — 천체 유형 분류 (2026-08-10)

- **문제:** SDSS 관측 데이터로 GALAXY/STAR/QSO 3-class 분류
- **평가지표:** Accuracy
- **대회 링크:** https://www.kaggle.com/t/06d6587e8496479ea184835edfffa74e (private community competition)
- **데이터 경로:** `/kaggle/input/datasets/yujaejun/day-01/` — zip 업로드 방식이라 대회 노트북에 자동 연결되지 않는다. Add Input 으로 직접 붙여야 한다

**데이터 스펙**
- train.csv 577,347행 × 12열, 결측치 없음
- test.csv 247,435행 × 11열(class 없음)
- 컬럼: id(int64), alpha·delta·u·g·r·i·z·redshift(float64), spectral_type·galaxy_population·class(범주형)
- spectral_type: O/B, A/F, G/K, M — 입력 피처
- galaxy_population: Red_Sequence, Blue_Cloud — 입력 피처
- class: GALAXY/STAR/QSO — 예측 타겟
- sample_submission.csv: id, class

**진행 방식:** 학습은 Kaggle 노트북에서 한다(로컬은 데이터 확인용). 첫 베이스라인은 RandomForestClassifier(n_estimators=300) + get_dummies.

## Day2 — 강수 여부 예측 (2026-08-11)

- **문제:** 기상 관측 데이터로 강수 여부 이진분류(rainfall 0/1)
- **평가지표:** AUC — Day1의 Accuracy와 다르다. `predict()` 가 아니라 `predict_proba()` 로 확률을 제출해야 한다
- **대회 링크:** https://www.kaggle.com/t/d4cea6668803405e89f515fb139edcd4

**데이터 스펙**
- train.csv 2,190행 — Day1(577,347행)보다 훨씬 작다. 과적합에 주의하고, 한 번의 train_test_split 보다 k-fold CV 가 안정적일 수 있다
- test.csv 에는 rainfall 없음, 결측치 없음
- 컬럼: id, day(1~365), pressure(999~1035hPa), maxtemp, temparature(평균기온 — **원본 오타 그대로**, temperature 아님), mintemp, dewpoint, humidity(39~98%), cloud(2~100%), sunshine(0~12.1h), winddirection(10~300도), windspeed(4.4~59.5)
- rainfall: 타겟. 학습 데이터의 약 75%가 1(비 내림) — 불균형 있음

**Day1에서 가져온 교훈:** 피처 엔지니어링보다 모델 구조 전환(배깅→부스팅)이 더 크게 작동했다. 노트북은 대회 자동연결이 안 되므로 zip 업로드 후 Add Input 이 필요하다. Save & Run All(Commit)은 새 세션이라 셀이 자체 완결형이어야 커밋이 실패하지 않는다.

## Day3 — 보험료 예측 (2026-08-12)

- **문제:** 보험료 예측. 첫 회귀 문제
- **평가지표:** RMSLE(낮을수록 좋음) — 로그 스케일 오차라 큰 이상치에 덜 민감하고, 과소예측보다 과대예측에 더 민감하다. 타겟(Premium Amount)을 `log1p` 로 변환해 회귀하고 `expm1` 로 되돌리는 접근이 유리하다
- **대회 링크:** https://www.kaggle.com/t/673d7adeb25e48c099ae8afe766f8c5b
- **블로그 보너스:** 이날은 +5점

**데이터 스펙**
- 약 120만 행 — Day1(57만), Day2(2,190행)과 규모가 다르다
- 여러 컬럼에 결측치 있음 — Day1·Day2와 달리 결측치 처리가 핵심 이슈일 수 있다
- 컬럼명에 공백 포함(예: "Annual Income", "Health Score") — `df['Annual Income']` 형태로 접근해야 한다
- 컬럼: id, Age, Gender, Annual Income, Marital Status, Number of Dependents, Education Level, Occupation, Health Score, Location, Policy Type, Previous Claims, Vehicle Age, Credit Score, Insurance Duration, Policy Start Date(날짜, 파생 피처 여지), Customer Feedback, Smoking Status, Exercise Frequency, Property Type, Premium Amount(타겟)
- 범주형이 많다(Gender, Marital Status, Education Level, Occupation, Location, Policy Type, Customer Feedback, Smoking Status, Exercise Frequency, Property Type) — 원핫 인코딩 시 차원과 카디널리티를 먼저 확인한다

**교훈:** 이전 결론(모델 선택, 피처엔지니어링 효과)을 새 데이터에 그대로 적용하지 말고 매번 처음부터 검증한다. 데이터 규모가 다르면(577K vs 2.2K vs 1.2M) 최적 전략이 완전히 달라지는 것이 반복 확인됐다.

## Day4 — 통신사 고객 이탈 예측 (2026-08-13)

- **문제:** Churn 이진분류
- **평가지표:** AUC(`predict_proba` 필요, Day2와 같은 형태)
- **대회 링크:** https://www.kaggle.com/t/e3ed9f91375d4b0f8c72c72b651b4147

**데이터 스펙**
- train 594,194행. 결측치 없음
- 타겟 Churn 은 원본이 Yes/No 문자열이라 **인코딩이 필요**하다(Yes=1)
- 클래스 불균형: Yes(이탈) 약 22.5%
- 21개 컬럼 중 16개가 범주형(gender, Partner, Dependents, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod + Churn)
- 수치형: SeniorCitizen(0/1), tenure(1~72), MonthlyCharges, TotalCharges
- 인터넷 미가입자는 부가서비스 컬럼이 "No internet service" 로 따로 표기된다(단순 No 가 아니다) — 카테고리가 3개인 컬럼에 주의
- sample_submission 의 Churn 컬럼은 **숫자(0~1 확률)** 를 기대한다. Yes/No 문자열이 아니다
- 데이터 로컬 경로: `C:\onedrive\_대학교\kaggle 대회\day-04\`

**교훈:** Day1(대규모·부스팅 유리), Day2(소규모·단순모델 유리), Day3(대규모·튜닝 후 LightGBM 역전, 검증조건 통일 중요, 결측지시자 효과적)의 패턴이 매번 달랐다. 59만 행은 Day2(2천)보다 크고 Day1·Day3(57만~120만)보다 작은 중간 규모다.

## Day5 — 교통사고 위험도 예측 (2026-08-14)

- **문제:** 회귀. 타겟 `accident_risk` 는 0~1 연속값(평균 약 0.35)
- **평가지표:** RMSE
- **마감:** 2026-08-14 23:55

**데이터 스펙**
- train 517,754행 × 14열, 결측치 없음
- 피처 12개: road_type, num_lanes, curvature, speed_limit, road_signs_present, public_road, lighting, weather, time_of_day, holiday, school_season, num_reported_accidents
- Boolean 컬럼 4개: road_signs_present, public_road, holiday, school_season

**핵심: 이 문제는 Kaggle Playground Series S5E10 "Predicting Road Accident Risk"(4,082팀 참가, 종료됨)의 재출제다.** 컬럼 구성과 평가지표가 완전히 일치하므로 외부 벤치마크를 그대로 쓸 수 있다.
- 공개된 3모델 스태킹(LGB+CatBoost+XGB → RidgeCV) CV RMSE 0.05600
- 그 모델의 Public LB 0.05553 = 상위 20%
- 즉 **평범한 GBDT와 상위 20%의 격차가 0.0005뿐인 포화 데이터**다(Day4와 같은 구조)

**외부 솔루션에서 확인된 유효 수단:** `speed_limit×curvature`, `num_lanes/(speed_limit+1)`, `num_reported_accidents/(num_lanes+1)`, 메타러너에 base 예측의 pairwise 곱·평균·std 추가, 자매대회 S5E12 1위의 Hill Climbing 가중치 최적화, S5E10 5위의 극단적 다중 fold.

**작업 폴더:** `C:\onedrive\_대학교\kaggle 대회\day-05\` — 계획서 `day-05_plan.md`, 실행순서 `README_실행순서.md`. 이 PC에는 Kaggle CLI 토큰이 없어 데이터는 직접 내려받아야 한다.

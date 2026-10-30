---
name: data-audit
description: Use right after loading a tabular or log dataset and before training anything. Checks leakage, duplicates, time order, missing-value meaning, class balance and distribution shift, and records each finding with evidence. Not a modeling step.
---

# Data audit (모델 전에 데이터부터)

각 점검은 명령 한 번으로 재실행할 수 있게 스크립트로 남긴다. 결과는 숫자로 적는다.

## 점검 목록

1. **모양.** 행·열 수, 자료형, 타깃 분포(양성 비율). 불균형이면 정확도는 지표로 쓰지 않는다.
2. **시간 순서.** 시간 열이 있는가? 정렬되어 있는가? 기간별 양성 비율이 변하는가? 순서가 있으면 무작위 분할을 의심한다.
3. **누수(leakage).** 판정 이후에만 알 수 있는 열, 타깃과 거의 1:1인 열, 이름에 결과·판정·hold·flag·label이 들어간 열을 찾는다. 단일 열만으로 성능이 비정상적으로 높으면 누수 후보다. 의심 열은 담당자에게 "이 값은 언제 기록되나요?"로 확인한다.
4. **중복.** 완전 중복 행, ID 중복, 특징은 같고 타깃이 다른 행. 중복이 학습/평가 양쪽에 걸치면 점수가 부풀려진다.
5. **결측.** 열별 결측률. 결측 자체가 정보인지(측정 생략) 확인한다. 결측 여부 지시 변수가 필요한지 판단한다.
6. **상수·준상수 열.** 분산 0 열은 근거를 남기고 제외한다.
7. **분포 변화.** 기간을 둘로 나눠 주요 열의 평균·결측률을 비교한다. 큰 변화가 있으면 그 시점을 담당자에게 묻는다.

## 기록

발견마다 `decision-log`에 한 줄: 무엇을 봤고, 숫자는 얼마이며, 어떻게 처리하기로 했는가. 처리하지 않기로 한 것도 이유와 함께 남긴다.

## 하지 말 것

- 점검 전에 모델부터 돌리기.
- 누수 열을 "성능이 좋아서" 남겨두기.
- 결측을 이유 없이 0이나 평균으로 채우기.

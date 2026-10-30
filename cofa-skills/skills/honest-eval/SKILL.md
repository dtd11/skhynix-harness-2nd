---
name: honest-eval
description: Use when setting up evaluation, comparing models, or before reporting any metric. Enforces a split that matches deployment (time-ordered when data has order), a metric at the operating constraint, a trivial baseline first, and an explanation of every number. Not for choosing features.
---

# Honest evaluation (숫자를 믿기 전에)

## 평가 틀

1. **분할은 실제 사용과 같게.** 데이터에 순서가 있으면 과거로 학습하고 미래로 평가한다. 튜닝은 학습 구간 안의 검증 구간에서만 한다. 테스트 구간은 마지막에 한 번 본다.
2. **지표는 운영 조건에서.** 담당자가 준 제약(예: 오탐률 ≤ x%, 하루 처리 k건)을 지표에 넣는다. 임계값은 검증 구간에서 정하고 테스트에는 그대로 적용한다. AUC 같은 요약 지표는 보조로만 쓴다.
3. **기준선 먼저.** 다수 클래스, 단순 규칙, 로지스틱 회귀 같은 가장 단순한 것의 숫자를 먼저 얻는다. 개선은 항상 기준선 대비 차이로 말한다.
4. **불확실성.** 양성이 적으면 숫자 하나가 크게 흔들린다. 양성 개수를 같이 적고, 가능하면 부트스트랩이나 여러 시점 분할로 범위를 낸다.

## 숫자 설명하기 (pstack의 explain-the-number 원칙을 이 상황에 맞게 옮김)

결과 숫자를 보고 다음에 답할 수 있어야 보고한다.

- 이 숫자가 실제로 무엇을 측정했나? 잘못된 분할, 누수 열, 중복, 임계값을 테스트에서 고른 것 때문은 아닌가?
- 왜 이보다 두 배 좋지 않은가? 무엇이 한계인가 (양성 수, 분포 변화, 특징 정보량)?
- 기준선과 차이가 잡음보다 큰가?
- 너무 좋으면 먼저 누수를 의심한다.

## 기록

`decision-log`에 실험마다 한 줄: 분할, 지표, 기준선 값, 이번 값, 차이의 이유.

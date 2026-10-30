---
name: minimal-solution
description: Use when deciding what to build or add after a baseline exists. Picks the simplest approach that meets the stated constraints and rejects extra models, layers, services or tuning that the stakeholder did not ask for. Not for evaluation design.
---

# Minimal solution (과설계 금지)

pstack의 laziness-protocol, subtract-before-you-add 원칙을 과제 상황에 맞게 옮겼다.

## 판단 규칙

- 제약 표의 항목 하나하나에 대해 "지금 방법이 이걸 만족하는가?"를 확인한다. 모두 만족하면 멈춘다.
- 새 요소(모델, 특징, 앙상블, 서버, 대시보드)를 더하려면 그것이 해결하는 제약 하나를 이름으로 말할 수 있어야 한다. 말할 수 없으면 더하지 않는다.
- 같은 성능이면 더 설명하기 쉬운 쪽을 고른다. 운영자가 이유를 물을 수 있는 과제라면 특히 그렇다.
- 지연 시간·하드웨어 제약이 있으면 실제로 재서 확인한다. 추정하지 않는다.
- 효과 없는 시도는 코드에서 지우고 기록에만 남긴다.

## 에이전트에게 맡길 때

- "가장 단순한 방법으로, 새 의존성 없이, 파일 하나에" 같은 범위를 같이 준다.
- 에이전트가 범위를 넘는 것을 만들면 되돌리고 이유를 기록한다.

## 하지 말 것

- 기준선 없이 복잡한 모델부터.
- 요청받지 않은 웹 UI, API 서버, 대규모 하이퍼파라미터 탐색.
- 0.1%p 개선을 위해 설명 가능성을 버리기.

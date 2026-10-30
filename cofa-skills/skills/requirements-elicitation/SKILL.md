---
name: requirements-elicitation
description: Use before any modeling when a stakeholder or scenario agent (담당자/실무자) knows requirements the README leaves out. Produces a short prioritized question list covering decision, metric, cost asymmetry, constraints, data meaning and deliverable. Not for writing the solution.
---

# Requirements elicitation (담당자에게 물을 것)

담당자는 물어본 것에만 답한다고 가정한다. 묻지 않은 조건은 채점 기준에 숨어 있다.

## 질문 영역 (위에서부터 우선)

1. **결정과 사용자.** 이 결과로 누가 무엇을 결정하는가? 결과를 받은 뒤 실제로 무슨 행동을 하는가?
2. **성공 지표.** 무엇으로 잘했다고 판단하는가? 정확도 하나인가, 특정 운영 조건에서의 값인가 (예: 오탐률 상한 아래의 재현율, 상위 k개 정밀도)?
3. **비용 비대칭.** 놓친 경우(FN)와 잘못 걸린 경우(FP)의 비용은 각각 어떤가? 처리 용량이나 하루 처리 한도가 있는가?
4. **운영 제약.** 지연 시간, 하드웨어(CPU/GPU), 배치인가 실시간인가, 설명 가능성이 필요한가?
5. **데이터 의미.** 행 하나는 무엇인가? 시간 순서가 있는가? 결측은 "측정 안 함"인가 "값 0"인가? 어떤 열이 판정 *이후*에 기록되는가? 기간 중 공정·정책 변경이 있었는가? 중복 행이 생기는 이유가 있는가?
6. **산출물.** 파일 이름·형식, 보고서 분량, 누가 읽는가?
7. **범위 밖.** 하지 않아도 되는 것은 무엇인가?

## 방법

- 질문은 한 번에 3~5개, 짧게, 예/아니오로 끝나지 않게 묻는다. "A와 B 중 어느 쪽이 더 비싼가요?"처럼 선택지를 준다.
- 답을 들으면 제약 표로 바꾼다: `제약 | 값 | 출처(담당자 답 n번) | 어떻게 확인할지`.
- 데이터를 보고 새로 생긴 의문은 2차 질문으로 다시 묻는다. 추측으로 메우지 않는다.
- 답을 못 받은 항목은 가정으로 적고 보고서의 가정 목록에 넣는다.

## 출력

질문 목록(우선순위 순)과, 답을 받은 뒤의 제약 표. 둘 다 `decision-log`에 남긴다.

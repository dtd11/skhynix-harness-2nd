---
name: task-workflow
description: Use at the start of a practical AI/data task whose README is incomplete and a stakeholder (담당자) holds hidden requirements. Sets the order of work (restate → ask → audit → baseline → minimal fix → verify → report) and the time budget. Not for one-off questions.
---

# Task workflow (숨은 요구사항이 있는 실무 과제)

사람이 판단하고, 에이전트는 실행과 확인을 맡는다. README를 통째로 넘기고 "해줘"로 끝내지 않는다.

## 순서

1. **목표 다시 말하기.** README를 읽고 3줄로 적는다: 누가 이 결과로 어떤 결정을 내리는가, 무엇이 성공인가, 아직 모르는 것은 무엇인가. 모르는 것 목록이 다음 단계의 질문이 된다.
2. **담당자에게 묻기.** `requirements-elicitation` 스킬로 질문을 만들고, 사람이 직접 담당자에게 보낸다. 답을 `decision-log`에 남긴다.
3. **데이터 점검.** `data-audit`. 모델보다 먼저 한다.
4. **기준선.** `honest-eval`. 가장 단순한 방법의 숫자부터 확보한다.
5. **최소 개선.** `minimal-solution`. 제약을 만족하는 가장 단순한 것만 더한다.
6. **검증.** `verify-before-submit`. 실제 산출물을 실행해서 확인한다.
7. **보고서.** `report-writer`. 결정에 필요한 내용만 1~2쪽.

각 단계가 끝날 때마다 결정 한 줄을 `decision-log`에 남긴다.

## 시간 배분 (180분 기준 예시)

| 구간 | 분 | 끝났다는 신호 |
|---|---|---|
| 읽기 + 목표 정리 + 1차 질문 | 0–25 | 질문 답을 받아 제약이 표로 정리됨 |
| 데이터 점검 | 25–50 | 누수·중복·순서·결측 판단 기록됨 |
| 기준선 + 평가 틀 | 50–80 | 운영 조건의 지표 숫자 1개 |
| 개선 1~2회 | 80–130 | 기준선 대비 차이와 그 이유 |
| 검증 + 보고서 | 130–165 | 산출물 재실행 통과, 보고서 완성 |
| 제출 준비 | 165–170 | 필수 파일·저장 상태 확인 후 제출 시작 |

에이전트 응답 시간도 예산이다. 긴 작업은 맡겨두고 그동안 다음 질문이나 보고서 뼈대를 쓴다.

## 프롬프트 습관

- 한 번에 한 가지 일을 맡긴다. 입력, 원하는 출력, 확인 방법을 같이 적는다.
- "왜 그렇게 했는지 한 줄로"를 붙여 근거를 받는다.
- 결과를 받으면 숫자와 파일을 직접 열어 확인한 뒤 다음으로 넘어간다.

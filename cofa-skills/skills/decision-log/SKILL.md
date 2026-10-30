---
name: decision-log
description: Use throughout a task to keep an append-only decision trail (what, why, evidence, result), and at the end to prepare for no-AI follow-up questions about the work. Use whenever a choice is made, a stakeholder answers, or an experiment finishes.
---

# Decision log (나중에 내 말로 설명하기 위해)

pstack의 show-me-your-work 아이디어를 짧게 옮겼다. 제출 뒤 AI 없이 "왜 그렇게 했나"를 답해야 하므로, 결정마다 이유를 그때 적는다.

## 형식

작업 폴더의 `DECISIONS.md`에 표로 한 줄씩 추가한다. 고치거나 지우지 않는다. 틀린 결정은 새 줄로 바로잡는다.

| 시각 | 단계 | 결정 | 이유 | 근거 | 결과 |
|---|---|---|---|---|---|

- **단계**: 질문 / 데이터 / 평가 / 모델 / 검증 / 보고서
- **이유**: 평범한 말로 한 문장. 담당자 답 번호나 제약을 직접 가리킨다.
- **근거**: 파일 경로, 명령, 숫자. 설명 문단이 아니다.
- **결과**: 숫자나 상태 (예: `recall 0.31 → 0.42`, `되돌림`, `미확인`).

`scripts/log.sh "<단계>" "<결정>" "<이유>" "<근거>" "<결과>"`로 한 줄을 붙일 수 있다.

## 언제 적나

담당자 답을 받았을 때, 데이터 처리 방식을 정했을 때, 실험 하나가 끝났을 때, 무언가를 하지 않기로 했을 때, 방향을 바꿨을 때. 사소한 명령은 적지 않는다.

## 마무리: 서술형 대비

제출 직전, 로그를 보고 받을 만한 질문 6개를 뽑는다 (예: 왜 이 분할인가, 왜 이 지표·임계값인가, 어떤 열을 왜 뺐나, 왜 더 복잡한 모델을 안 썼나, 결과의 한계는, 데이터가 바뀌면 무엇이 깨지나). 각 질문에 근거 숫자 하나가 들어간 세 문장 답을 사람이 직접 소리 내어 정리한다. 답은 AI가 대신 써 주지 않는다. 로그에 이유가 비어 있는 결정이 있으면 지금 채운다.

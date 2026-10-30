---
name: report-writer
description: Use when writing the final report or README for a stakeholder. Produces a 1–2 page decision-oriented document with recommendation, numbers at the operating constraint, assumptions, limits and next steps. Not for code comments or logs.
---

# Report writer (결정을 돕는 1~2쪽)

읽는 사람은 담당자다. 결론부터 쓴다.

## 구조

1. **한 줄 결론.** 무엇을 권하는가, 그 근거 숫자 하나.
2. **문제와 제약.** 담당자에게 확인한 제약 표 요약 (지표, 운영 조건, 지연, 설명 가능성).
3. **데이터에서 발견한 것.** 누수·중복·결측·분포 변화와 처리 방법. 숫자로.
4. **방법.** 기준선과 최종 방법, 왜 이것이 충분한지 (더 복잡한 것을 안 한 이유 포함).
5. **결과.** 운영 조건에서의 값, 기준선 대비 차이, 불확실성 범위. 표 하나.
6. **가정과 한계.** 확인 못 한 것, 데이터가 바뀌면 깨질 수 있는 것.
7. **다음 단계.** 운영에 넣기 전 확인할 것, 모니터링할 지표.
8. **재현 방법.** 실행 명령 한두 줄.

## 문체

- 짧은 문장, 숫자는 단위와 함께. 과장 표현 없이.
- 모든 숫자는 실제 실행 결과에서 가져온다. 추정치는 추정이라고 적는다.
- `decision-log`의 행을 근거로 쓴다.

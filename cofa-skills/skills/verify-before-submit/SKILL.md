---
name: verify-before-submit
description: Use before declaring any step done and before final submission. Verifies the real artifact by running it from a clean state, reading actual outputs, and checking required files against the task instructions. Not for exploring ideas.
---

# Verify before submit (진짜로 돌아가는지)

pstack의 prove-it-works 원칙: 대리 신호(에이전트의 "완료했습니다", 컴파일 성공, 파일이 있다는 사실)가 아니라 실제 산출물을 확인한다.

## 단계마다

- 에이전트가 끝났다고 하면 결과 파일을 직접 열고, 숫자를 다시 계산하는 명령을 한 번 돌린다.
- 확인 명령은 스크립트로 남겨 다시 돌릴 수 있게 한다.

## 제출 전 체크리스트

1. 새 터미널에서 처음부터 한 번에 실행된다 (학습 → 평가 → 결과 파일 생성).
2. 결과 숫자가 보고서에 적힌 숫자와 같다.
3. 과제 안내의 필수 파일 이름·경로·형식이 모두 맞다.
4. 지연 시간 같은 제약은 실제로 잰 값이 있다.
5. 편집기 저장 상태가 모두 "저장됨"이다. 외부 변경 충돌이 없다.
6. 임시 파일, 쓰지 않는 실험 코드, 큰 중간 산출물은 정리했다.
7. 보고서의 가정·한계가 실제 구현과 맞다.

실패하면 증상이 아니라 처음 잘못된 지점을 고친다 (pstack의 fix-root-causes).

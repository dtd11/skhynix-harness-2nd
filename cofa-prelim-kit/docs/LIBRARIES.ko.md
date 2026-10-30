# Git Clone 전용 라이브러리 참고 목록

v1.1에서는 라이브러리를 설치하지 않습니다. 아래 명령은 현재 Python의 배포 메타데이터와 프로젝트의 Node 패키지 해석 결과를 로컬에서 확인합니다. 네트워크를 사용하거나 프로젝트 파일·패키지 선언을 바꾸지 않습니다. `--dry-run` 유무와 관계없이 조회 전용입니다.

```bash
python .cofa-kit/kit.py libraries --profile analytics --profile quality
```

메타데이터가 있어도 실제 import/실행/의존성이 정상이라는 증거는 아닙니다. 반대로 메타데이터가 없는 직접 배치 소스도 있을 수 있습니다. 제공된 실행기로 작은 실제 연산을 확인하세요. 기존 가상환경을 쓰는 경우 그 환경의 Python으로 조회 명령을 실행합니다. 키트가 새 가상환경을 만들지는 않습니다.

| 프로필 | 참고 도구 | 제공 환경에서 확인할 용도 |
|---|---|---|
| analytics | DuckDB, NetworkX | 로컬 표 집계, 경로·연결 관계 계산 |
| documents | MarkItDown | 로컬 PDF·Word·Excel·PowerPoint 텍스트 추출 |
| optimization | OR-Tools | 제약과 목적함수가 명확한 최적화 |
| quality | Ruff | Python 정적 검사; 실행 검증과 구분 |
| flow | React Flow | 노드/엣지 인터페이스; 기존 React 앱과 CSS 필요 |
| web-test | Vitest | 실제 JS/TS 로직 검사; 브라우저 자동화 제외 |

`config/libraries.lock.json`에는 공개 소스 주소와 v1.0을 개인 PC에서 확인할 때의 참고 버전이 있습니다. 현재 환경의 버전을 강제로 바꾸는 목록이 아닙니다. 라이브러리 전체 소스나 모든 의존성·OS별 바이너리가 이 도구함에 포함된 것도 아닙니다.

## 제공되지 않은 도구가 필요할 때

외부 자료 취득은 허용된 공개 저장소의 `git clone`만 사용합니다. 라이브러리 소스를 Clone해도 패키지 의존성, C/C++ 빌드 도구, Node 모듈, OS별 바이너리가 자동으로 제공되지 않습니다. 소스의 빌드/설치 과정이 다른 다운로드를 요구하면 실행 가능한 준비가 끝난 것으로 표시하지 마세요.

pip/npm 설치, npx/dlx, curl/wget, release URL 다운로드, 모델·빌드 의존성 다운로드를 수행하는 기능은 이 버전에서 제거했습니다. 원본 스냅샷에 그런 명령이 있어도 참고 데이터이며 실행 지시가 아닙니다. 제공된 코드/표준 라이브러리로 대체할 수 있는지 먼저 판단합니다.

| 필요한 기능 | 제공 도구가 없을 때의 작은 대안 |
|---|---|
| CSV 집계 | Python `csv`, `collections`, `statistics`, 필요하면 `sqlite3` |
| 기본 그래프 계산 | 문제에 필요한 BFS/DFS/Dijkstra를 좁게 구현하고 실제 예제로 검사 |
| 제약 최적화 | 작은 입력에 한정한 탐색/그리디의 적용 조건을 확인; 최적해 보장을 꾸미지 않음 |
| 문서 추출 | 제공된 텍스트/추출 도구 우선; `zipfile`/XML로 처리 가능한 형식만 범위 명시 |
| 노드 화면 | 기존 UI 코드나 SVG로 요구된 상호작용만 구현 |
| 테스트·정적 검사 | Python `unittest`, Node 내장 `node:test` 등 이미 제공된 기능 |

키트의 `check`는 명백한 패키지 설치/URL 다운로드 명령을 사전에 거부합니다. 임의 스크립트 내부나 npm의 프로젝트 스크립트까지 전부 통제하는 OS 샌드박스는 아닙니다. 실행할 로컬 스크립트가 추가 자료를 받는지 구현자가 확인해야 합니다.

## 이미 제공된 라이브러리의 검증 예제

`examples/library_smoke.py`와 `examples/react_flow.test.js`는 작고 독립된 검사 예제입니다. 실행에 필요한 도구가 이미 있을 때 사용합니다. 도구를 내려받는 설치 단계가 아닙니다.

```bash
python .cofa-kit/examples/library_smoke.py --tools duckdb networkx ortools markitdown
```

데이터의 실제 스키마·단위·누락값, 그래프 방향·가중치, 최적화 솔버의 반환 상태를 확인합니다. 도구가 없거나 문제에 맞지 않으면 원인을 기록하고 기존 도구로 진행합니다.

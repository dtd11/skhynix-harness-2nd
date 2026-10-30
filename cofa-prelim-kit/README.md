# COFA 예선 개발 키트

처음 공개되는 서비스·코드 과제를 제공된 Codex로 구현하기 위한 **Git Clone 전용 도구함 v1.1.0**입니다. 공개 저장소 [arcturus0637-rgb/cofa-prelim-kit](https://github.com/arcturus0637-rgb/cofa-prelim-kit)를 시험 환경에서 `git clone` 한 번으로 가져옵니다. 스킬·하네스는 추가 다운로드 없이 로컬에서 등록합니다. 제공된 Python 3.10 이상을 사용하며 계정·API 키·MCP·모델 프록시가 필요하지 않습니다.

선택한 공개 원본 7개를 커밋 단위로 보관하고, 대회에서 사용할 8개 스킬로 연결했습니다. 원본은 `upstream/`에 보관하며 자동 활성화하지 않습니다. React Flow·DuckDB·MarkItDown·Vitest·Ruff·NetworkX·OR-Tools는 제공 환경의 기존 패키지를 확인하는 참고 목록입니다. 이 라이브러리들의 실행 코드·모든 의존성·바이너리가 이 저장소에 포함된 것은 아닙니다. 소스를 Clone해도 실행 준비가 자동으로 끝나는 것은 아닙니다.

참가자가 외부 자료 취득은 Git Clone만 허용된다고 확인해, v1.0의 pip/npm 선택 설치 기능을 제거했습니다. `libraries`는 이제 **조회 전용**입니다. 원본의 설치 안내나 npx/curl 명령도 수행하지 않습니다. 빌드 과정이 별도 의존성을 내려받는 경우에도 실행 준비가 됐다고 간주하지 않습니다.

## 가져갈 내용

| 역할 | 구성 |
|---|---|
| 전체 작업 흐름 | `cofa-prelim`: 문제 분석·핵심 구현·시간 안배·제출 준비 |
| 디버깅 | Superpowers systematic-debugging + Matt diagnosing-bugs |
| 단순화 | code-simplifier + Ponytail + Karpathy-inspired 지침 |
| 리뷰 | Matt/Ponytail/Caveman의 변경 범위 중심 리뷰 |
| 검증 | Superpowers 검증 + 실행 로그·소스 변경 감지 |
| 데이터·그래프·문서 | 선택한 7개 라이브러리의 기존 설치 상태와 사용 안내 |
| SQL | Supabase/PostgreSQL 지침; 클라우드 연결은 설치하지 않음 |
| 간결한 대화 | Caveman의 간결성만 적용; 코드·오류·숫자·문서는 압축하지 않음 |

기존 묶음으로 디버깅·단순화·리뷰가 충분히 겹쳐 추가 대형 하네스를 도입하지 않았습니다. 관련 Caveman의 investigate-first·surgical-patch·safe-refactor 등도 원본 참고자료로 보관했습니다. [원본 목록과 변경 범위](docs/SOURCES.ko.md)

## 사전 체험에서 설치

공개 GitHub 저장소로 올릴 때 **이 폴더 전체를 저장소의 루트**로 사용합니다. 시험에서는 ZIP이나 개인 파일을 업로드하지 않고 그 공개 저장소를 Clone합니다. `install` 명령은 Clone한 파일의 로컬 배치만 수행하며 패키지 설치나 다운로드를 하지 않습니다. `PROJECT`는 실제 과제 경로로 바꾸세요. Linux에서는 `python` 대신 `python3`가 필요할 수 있습니다.

```bash
git clone https://github.com/arcturus0637-rgb/cofa-prelim-kit.git
python cofa-prelim-kit/kit.py verify-bundle
python cofa-prelim-kit/kit.py install --project /path/to/PROJECT --dry-run
python cofa-prelim-kit/kit.py install --project /path/to/PROJECT
cd /path/to/PROJECT
python .cofa-kit/kit.py doctor
```

실제 과제 폴더 안의 `tools/cofa-prelim-kit`처럼 Clone해도 됩니다. 설치 대상은 과제 폴더이고, 키트 폴더 자체나 그 하위는 설치 대상으로 지정하지 마세요. 키트 폴더에서 앱을 시작하도록 과제 구조를 바꾸지 않습니다.

설치 결과는 `.agents/skills/cofa-*`, `.cofa-kit/`, 기존 내용을 보존한 `AGENTS.md`입니다. 원본 `AGENTS.md`는 `.cofa/AGENTS.before-kit.md`로 보관합니다. 다른 내용의 기존 스킬/키트 파일이 있으면 덮어쓰지 않고 멈춥니다. 같은 버전 재설치는 같은 결과를 냅니다. 전역 Codex 설정은 수정하지 않습니다. 실행 중인 Codex가 스킬을 발견하지 못하면 제공 환경의 안내에 따라 새 세션에서 확인하세요.

사전 체험의 작업이 본 과제로 보존된다는 보장은 없습니다. 실제 과제 시작 후 필요하면 다시 Clone하고 로컬 등록하세요. 준비에 드는 시간도 실제 작업 시간에 영향을 줍니다. Python이 없다면 추가로 내려받지 말고 Codex에 저장소의 `skills/cofa-prelim/SKILL.md`를 직접 읽도록 요청하세요. 이 경우 Python CLI의 시간/증거 관리 기능은 사용할 수 없습니다.

## Codex에 줄 시작 요청

아래 요청에 **실제 과제와 시작 시각**을 덧붙이면 됩니다. 과제를 읽기 전부터 완성 앱이나 결과물을 끼워 넣는 키트가 아닙니다.

```text
$cofa-prelim을 사용해 이 과제를 구현해줘.
README와 실제 제출 요구사항부터 읽고 제공된 구조를 유지해.
필수 기능을 끝까지 연결한 뒤 남은 시간에 맞춰 검증과 제출 준비를 해.
디버깅·단순화·리뷰 스킬은 필요할 때만 읽어.
브라우저 조작은 내가 플랫폼 미리보기에서 직접 확인할게.
실제 과제 시작 시각: YYYY-MM-DDTHH:MM:SS+09:00
```

과제 시작 전에는 `start`를 실행하지 않습니다. `start`는 플랫폼 타이머를 시작하거나 변경하지 않고 이미 시작된 시각을 기록합니다. 상세 가이드상 **과제 시작과 함께 작업 타이머가 시작**됩니다. 서술형의 별도 시작 버튼과 구분하세요.

## 기존 라이브러리 확인

필요한 라이브러리가 제공 환경에 이미 있는지 로컬 메타데이터만 확인합니다. 패키지를 불러와 실행하는 검사도, 설치도 아닙니다.

```bash
python .cofa-kit/kit.py libraries --profile analytics
```

| 조회 프로필 | 확인 대상 |
|---|---|
| analytics | DuckDB, NetworkX |
| documents | MarkItDown의 로컬 PDF·DOCX·XLSX·PPTX 처리 |
| optimization | OR-Tools |
| quality | Ruff |
| flow | React Flow (`@xyflow/react`) |
| web-test | Vitest |

현재 실행 중인 Python의 패키지 메타데이터와 프로젝트의 Node 패키지 해석 결과를 확인합니다. 파일·의존성 선언을 바꾸지 않습니다. 없으면 제공된 도구나 표준 라이브러리로 대체합니다. Git Clone한 라이브러리 소스도 의존성과 OS별 실행 조건이 충족돼야 쓸 수 있습니다. [자세한 사용법](docs/LIBRARIES.ko.md)

## 작업 중 사용

```bash
python .cofa-kit/kit.py start --started-at 2026-10-31T10:00:00+09:00 --kind web
python .cofa-kit/kit.py status
python .cofa-kit/kit.py require --id R1 --text "실제 과제에서 요구한 기능"
python .cofa-kit/kit.py check --name unit -- npm test -- --run
python .cofa-kit/kit.py require --id R1 --status verified --evidence E1
```

`E1`은 예시입니다. 명령 출력에 나온 실제 증거ID를 사용해야 합니다. 실패/시간 초과를 성공으로 기록하지 않으며 코드가 바뀌면 이전 결과는 오래된 증거로 표시됩니다. 전체 로그는 `.cofa/logs`에 남습니다. 명령은 직접 허용 범위를 판단해 전달하세요. 이 도구는 임의 명령의 모든 동작을 통제하는 OS 샌드박스가 아닙니다.

참가자가 실제로 플랫폼 미리보기를 확인한 뒤에만 관찰 내용을 기록합니다.

```bash
python .cofa-kit/kit.py manual --name manual-ui --result pass --note "참가자가 확인한 구체적인 동작"
python .cofa-kit/kit.py handoff --required-file README.md
```

필수 파일명은 과제 기준입니다. `README.md`도 예시입니다. `handoff`는 로컬 체크리스트이며 플랫폼 제출을 수행하지 않습니다. 미리보기에서 저장 상태·제출 목록을 직접 확인하세요.

**플랫폼에서 제출물을 확정한 뒤** 다음 명령으로 상태를 기록합니다. 실제 버튼을 누르지 않고 실행하면 잘못된 상태가 기록됩니다.

```bash
python .cofa-kit/kit.py stage --to locked
```

확정 이후 작업과 서술형 답변에는 AI를 사용하지 않습니다. 로컬 도구의 단계 기록도 규칙 안내를 위한 보조 기능이며 플랫폼의 차단 기능을 대신하지 않습니다.

## 연습 및 확인 범위

연습용 폴더를 별도로 만들고 `start --practice --kind web`을 사용하면 현재 시각 기준으로 연습 타이머를 기록합니다. 실제 세션을 초기화하거나 되돌리는 명령은 없습니다.

```bash
python -m unittest discover -s tests -v
python kit.py verify-bundle
```

[검증 기록](docs/VALIDATION.ko.md)은 이 PC에서 관찰한 결과와 미확인 범위를 구분합니다. 시험장의 Linux/네트워크/권한은 사전 체험에서 확인해야 합니다. [대회 규칙과 시간 계산](docs/EXAM_RULES.ko.md), [작업 흐름](docs/WORKFLOW.ko.md)

원본 7개는 각 원본 라이선스를 유지합니다. 새 하네스·어댑터·스크립트만 루트 MIT 라이선스를 따릅니다. 개인 설정·키·기존 작업 기록·시험 PDF·문제·응시 산출물은 이 공개 배포물에 포함하지 않습니다. `.gitattributes`는 Windows/Linux 간 Clone 시 무결성 해시의 바이트를 유지합니다. [시험 전 공개 저장소 준비](docs/GITHUB.ko.md)

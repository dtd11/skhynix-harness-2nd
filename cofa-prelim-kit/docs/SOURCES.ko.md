# 원본과 선택 범위

정확한커밋/경로는`config/sources.lock.json`,각배포파일의SHA-256은`bundle-lock.json`에있습니다. 원본파일내용은변경하지않았고선택한경로만보관했습니다. `skills/cofa-*`는이키트에서새로작성한대회용연결지침입니다. 원본전체워크플로를모두활성화하지않습니다.

| 원본 | 보관범위 | 적용방식 |
|---|---|---|
| https://github.com/obra/superpowers | systematic-debugging, verification-before-completion와해당지원파일 | 원인조사·검증지침을필요할때참조 |
| https://github.com/anthropics/claude-plugins-official | code-simplifier에이전트원문과라이선스 | Codex용cofa-simplify에서원문참조;Claude실행안함 |
| https://github.com/mattpocock/skills | engineering전체와handoff | 기본은diagnosing-bugs/code-review/tdd등필요한것만참조;외부이슈/PR/설정자동실행안함 |
| https://github.com/supabase/agent-skills | supabase, supabase-postgres-best-practices | SQL/실제제공Supabase환경에한해참조;클라우드계정생성안함 |
| https://github.com/multica-ai/andrej-karpathy-skills | karpathy-guidelines | Karpathy발언에서영감을받은제3자지침;Karpathy본인제작/공식배포로표시안함 |
| https://github.com/DietrichGebert/ponytail | ponytail, review, audit, debt | 최소완전변경·행동보존단순화;hook/프록시설치안함 |
| https://github.com/JuliusBrussee/caveman | 기본voice/review, investigate-first, lean-build, surgical-patch, safe-refactor, verify-and-stop | 간결한설명/국소수정참고;CLI·라우팅·브라우징·클라우드·텔레메트리제외 |

원본에있는설치명령/전역설정/외부API/다른모델/브라우저자동화지시는수행지시가아닌참고자료입니다. 실제과제/플랫폼/호스트권한과대회용어댑터의범위를먼저확인합니다. 원본의유용한기술적방법만선택합니다.

각원본LICENSE/NOTICE와하위라이선스를보존했습니다. Karpathy-inspired원본은SKILL프런트매터에MIT를선언하지만해당커밋에루트LICENSE본문은없어이사실을`LICENSE-DECLARATION.txt`에기록했습니다. 나머지원본의MIT/Apache등조건은각스냅샷원문을확인하세요. 새코드는루트LICENSE를따르고제3자원본의조건을대체하지않습니다.

`config/libraries.lock.json`의ReactFlow,DuckDB,MarkItDown,Vitest,Ruff,NetworkX,OR-Tools는사용자가선택한라이브러리입니다. 개인 PC에서 확인한 참고 버전과 원본 주소를 보관했으며 전체 실행 코드를 복사하지는 않았습니다. v1.1은 Git Clone 전용이며 추가 패키지 설치를 하지 않습니다. 제공 환경의 기존 도구를 사용합니다.

추가디버깅/단순화프로젝트는불필요하다고판단했습니다. 이미Superpowers+Matt의진단,code-simplifier+Ponytail+Karpathy의단순화,Caveman의국소수정참고가겹칩니다. 원본의벤치마크수치/토큰절약주장은이키트나대회환경에서재현했다고표시하지않습니다.

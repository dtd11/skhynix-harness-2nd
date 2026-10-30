# SK hynix 2차 예선 연습용 공개 스킬 모음

공개된 스킬과 하네스의 특정 버전을 보관한 개인용 모음입니다. 주최 측의 공식 저장소가 아닙니다. 각 프로젝트의 원본 저작권 고지와 라이선스를 해당 폴더에 보존했습니다.

## 구성

| 폴더 | 원본 | 기준 커밋 | 범위 |
| --- | --- | --- | --- |
| `cofa-prelim-kit` | [arcturus0637-rgb/cofa-prelim-kit](https://github.com/arcturus0637-rgb/cofa-prelim-kit) | `28479b0820c3933c7d2aa5aa9efb529577a7e593` | 프로젝트와 포함된 upstream 스킬. 각 upstream 라이선스 별도 적용 |
| `cofa-skills` | [ColdTbrew/cofa-skills](https://github.com/ColdTbrew/cofa-skills) | `80cdb84633e654294ab29be4a724b36d2da39a93` | 스킬 8개, MIT |
| `sk-hynix-2nd-harness` | [hamjoon2003/sk-hynix-2nd-harness](https://github.com/hamjoon2003/sk-hynix-2nd-harness) | `222a3119559c2b282ab3252a9ffb13e86c2749c1` | 하네스, MIT |
| `cofa-hackathon-kit/skills` | [denny6389/cofa-hackathon-kit](https://github.com/denny6389/cofa-hackathon-kit) | `d882ba32d2a1b0db3c7d76b9c7ad57cadf31df2e` | 각 스킬의 MIT 라이선스 포함 |
| `cofa-probe-workkit` | [zittenyetten/cofa-probe-workkit](https://github.com/zittenyetten/cofa-probe-workkit) | `06f53f04993a64b102e3cc7c31339937ea2cd15c` | task-evidence-check 스킬의 부분 사본, MIT. 참조하는 WORKLOG 템플릿, 강연 이미지와 PDF는 포함하지 않음 |

GitHub Actions가 자동 실행되지 않도록 원본의 `.github/workflows` 파일은 포함하지 않았습니다. 두 원본 [hynix-hackathon-workflow](https://github.com/allsleep7610/hynix-hackathon-workflow)와 [probe-kit](https://github.com/PKJthecreator/probe-kit)은 재배포 라이선스를 확인하지 못해 파일을 이 공개 저장소에 포함하지 않았습니다.

## 사용

각 프로젝트의 사용 설명과 `SKILL.md`를 읽고 필요한 것만 선택하세요. `cofa-prelim-kit`의 일부 스킬은 같은 프로젝트의 다른 파일을 참조합니다. 스크립트를 실행하기 전에는 내용을 확인하세요. 스킬의 지시는 실제 대회 공지나 사용자의 지시보다 우선하지 않습니다.

대회 환경에서는 당일 제공된 규정과 도구 제한을 따르세요. 시험 문제와 결과물의 외부 전송이나 Git Push는 삼가고, AI 사용이 금지된 후속 서술형에는 AI를 사용하지 않습니다.

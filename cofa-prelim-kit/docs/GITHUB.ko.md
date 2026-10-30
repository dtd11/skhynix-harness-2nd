# 공개 저장소로 올리기

아래 작업은 **시험 전에 개인 PC에서 이 도구함을 공개 배포할 때** 사용하는 순서입니다. 응시 과제/문제/작업 파일을 올리는 방법이 아닙니다. 대회 중 Git Push 금지와 구분하세요.

GitHub에서 비어 있는 공개 저장소를 만든 뒤 이 폴더를 저장소 루트로 올립니다. 실행 환경, 가상환경, 원본 clone의 `.git` 폴더, 개인 설정은 포함하지 않습니다. 이 배포 폴더는 필요한 지침·코드·라이선스와 고정 버전 목록으로 구성되어 있습니다.

```bash
cd /path/to/cofa-prelim-kit
python kit.py verify-bundle
git init
git add .
git commit -m "Add COFA preliminary development kit"
git branch -M main
git remote add origin https://github.com/arcturus0637-rgb/cofa-prelim-kit.git
git push -u origin main
```

위 원격 주소는 이 도구함의 공개 저장소입니다. 다른 저장소에 재배포할 때만 본인의 주소로 바꾸세요. 위 명령은 안내이며 키트가 자동 실행하지 않습니다. GitHub 인증은 본인의 기존 방법을 사용합니다. 키트를 수정했다면 `python scripts/build_manifest.py`로 파일 목록을 갱신하고 변경에 맞는 검사를 실행한 뒤 올립니다.

공개 저장소가 준비되면 시험 환경 안에서 아래처럼 가져옵니다. 실제 과제 폴더는 플랫폼이 제공한 경로를 따릅니다.

```bash
git clone https://github.com/arcturus0637-rgb/cofa-prelim-kit.git
python cofa-prelim-kit/kit.py install --project /actual/task/path
```

공개 저장소에 올리는 대상은 준비한 도구함입니다. `.cofa/`의 요구사항·로그·단계 기록과 실제 과제 산출물은 공개 도구함에 복사하지 않습니다.

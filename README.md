# 학교 방문자 사전 등록
1. Google Sheets에서 빈 스프레드시트를 생성하고 URL의 /d/와 /edit 사이 ID를 복사합니다.
2. 확장 프로그램 → Apps Script에서 Code.gs 내용을 붙여넣습니다.
3. 프로젝트 설정 → 스크립트 속성에 SPREADSHEET_ID와 API_TOKEN을 추가합니다. 토큰은 `python -c "import secrets; print(secrets.token_hex(32))"`로 생성합니다.
4. 배포 → 새 배포 → 웹 앱 → 실행 사용자: 나, 액세스 권한: 모든 사용자(익명 포함). 권한 승인 후 /exec URL을 복사합니다.
5. GitHub 저장소에 app.py, requirements.txt, Code.gs, README.md, .gitignore를 업로드합니다.
6. https://share.streamlit.io 에서 저장소, main 브랜치, app.py를 선택합니다. Advanced settings → Secrets에 아래 값을 입력하고 배포합니다.
```toml
APPS_SCRIPT_URL = "https://script.google.com/macros/s/실제배포ID/exec"
API_TOKEN = "스크립트 속성과 동일한 토큰"
```
로컬 실행 시 위 TOML을 .streamlit/secrets.toml에 저장하고 `python -m pip install -r requirements.txt`, `python -m streamlit run app.py`를 실행합니다.
등록 성공 후 방문자등록 시트가 생성됩니다. QR은 등록번호만 포함하며 관리자 시트에서 대조합니다. QR 자체는 출입 승인이나 본인 인증 수단이 아닙니다.
실제 운영 전 학교 개인정보 담당자와 보유기간, 문의처, 동의 문구, 접근권한 및 삭제 절차를 확정하세요. 공개 앱의 무단 등록 방지 대책도 필요합니다. 구글 계정 정책에 따라 익명 웹 앱 배포가 제한될 수 있습니다. 실제 계정 연동 테스트는 배포 후 진행해야 합니다.

# 💌 Wedding Guest Manager (축의금 정산 매니저)

친누나의 결혼식 축의대를 맡게 되면서 효율적으로 정산을 하기 위해 개발한 축의금 정산 프로그램입니다.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blue?style=flat)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?style=flat&logo=pandas&logoColor=white)

## 📌 Project Overview
- 결혼식 당일, 접수대에서 수기로 작성하던 방명록의 비효율성을 개선하기 위해 기획
- 빠른 하객 등록, 실시간 축의금 합계 계산, 식권 배부 현황 파악, 그리고 정산용 엑셀 리포트 자동 생성 기능을 제공

실제 가족의 결혼식에서 사용하기 위해 **현장의 긴박함과 사용성(UX)**을 최우선으로 고려하여 설계되었습니다.

## 📸 Screenshots
| 메인 대시보드 & 통계 | 하객 등록 창 |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/454da7ea-33ca-4de7-ba14-453b5e5f7393" width="500"/> | <img src="https://github.com/user-attachments/assets/5b7a7508-3eab-4b1e-b33e-a23b1671e0c5" height="400"/> |
| **엑셀 정산 리포트** | **엑셀 정산 리포트** |
| <img src="https://github.com/user-attachments/assets/dac58d35-58e1-427b-908d-0ea6529d83fe" width="500"/> |<img src="https://github.com/user-attachments/assets/84d00eed-1ae1-44c7-aa5b-ed13a44875e0" width="500"/> |





## ✨ Key Features

### 1. 직관적인 하객 관리 (CRUD)
- **빠른 등록:** 이름, 소속, 관계 등 필수 정보를 신속하게 입력.
- **퀵 버튼:** [+1만], [+5만] 등 자주 쓰는 금액을 버튼으로 제공하여 타이핑 최소화.
- **수정 및 삭제:** 오기입 시 즉시 수정 및 데이터 안전 삭제 기능.

### 2. 실시간 통계 대시보드
- **자동 집계:** 전체 인원, 식권 배부 수량, 총 축의금 액수를 실시간으로 확인.
- **다이나믹 뷰:** [대상별(신랑/신부)] 및 [관계별(친구/친척)] 통계를 토글 버튼으로 즉시 전환하여 조회.
- **UI 안정성:** 데이터 양에 관계없이 깨지지 않는 견고한 레이아웃 설계.

### 3. 강력한 데이터 관리 및 내보내기
- **엑셀 리포팅:** `Pandas`와 `OpenPyXL`을 활용하여 스타일링(테두리, 헤더 색상)이 적용된 엑셀 파일 생성.
- **시트 분리:** [전체 명단]과 [요약 통계] 시트를 자동으로 분리하여 저장.
- **JSON 기반 저장:** 별도의 DB 설치 없이 로컬 JSON 파일로 가볍고 안전하게 데이터 영구 저장.

### 4. 사용자 편의성
- **확장 가능한 설정:** 관계(친구, 직장 등)나 구분(신랑, 신부) 항목을 사용자가 직접 추가/삭제 가능.
- **스마트 검색:** 이름, 소속 등 키워드로 하객 명단 초고속 필터링.
- **파일 잠금 방지:** 엑셀 파일이 열려 있을 경우 예외 처리를 통해 프로그램 강제 종료 방지.

## 🛠 Tech Stack

- **Language:** Python 3.x
- **GUI Framework:** CustomTkinter (Modern UI)
- **Data Processing:** Pandas, OpenPyXL
- **Build Tool:** PyInstaller
- **VCS:** Git

## 📂 Project Structure

```bash
Wedding-Gift-Manager/
├── main.py              # 프로그램 진입점 (UI 및 메인 로직)
├── data_manager.py      # 데이터(JSON) 로드 및 저장 관리
├── add_dialog.py        # 하객 추가/수정 팝업창 UI
├── settings_dialog.py   # 카테고리 설정 관리 UI
├── about_dialog.py      # 프로그램 정보 및 크레딧
├── icon.ico             # 애플리케이션 아이콘
└── guest_data.json      # (자동생성) 하객 데이터 저장소
```

## 🚀 How to Run
### 1. 개발 환경에서 실행

```Bash
# 필수 라이브러리 설치
pip install customtkinter pandas openpyxl


# 실행
python main.py
```

### 2. 실행 파일(EXE) 빌드 방법
```Bash
pip install pyinstaller

# 빌드 명령어 (아이콘 포함, 콘솔 미노출)
pyinstaller --noconsole --onefile --collect-all customtkinter --icon="icon.ico" --name "축의금매니저" main.py
```
## ⚠️ Privacy Note
```
guest_data.json 파일에는 실제 하객들의 개인정보와 축의금 내역이 포함되므로, 절대 GitHub 저장소에 업로드하지 마십시오. (이미 .gitignore 처리가 되어 있습니다.)
```
## 👨‍💻 Developer

Seyoung Backend Developer Aspiring to build robust and scalable systems.

[GitHub: github.com/syann97](https://github.com/syann97)

© 2026 Seyoung. All Rights Reserved.

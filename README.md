# 🏥 Dr-AI-Sentinel (Dr. AI Sentinel)

> **Automated Medical Research Surveillance System running on Synology NAS.** > 시놀로지 NAS 기반 재활의학 논문 및 임상시험 24시간 자동 모니터링 시스템

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Synology](https://img.shields.io/badge/Platform-Synology%20NAS-gray)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Overview (개요)
**Dr-AI-Sentinel**은 재활의학과 전문의를 위해 개발된 **지능형 의료 정보 수집 봇**입니다.  
매일 아침 7시, 전 세계의 의학 데이터베이스를 검색하여 사용자가 지정한 키워드(재활, 뇌졸중, DTx 등)와 관련된 최신 정보를 수집하고, **Telegram**과 **Email**로 요약 보고서를 발송합니다.

## ✨ Key Features (핵심 기능)
* **📘 Journal Bot:** PubMed(ARM) 및 주요 저널(APMR) RSS 트래킹.
* **💊 Clinical Bot:** ClinicalTrials.gov API v2를 활용한 최신 임상시험 검색.
* **�� ArXiv Bot:** 'Deep Learning' + 'Rehabilitation' 관련 최신 AI 논문 감시.
* **🧪 Trials Bot:** WHO/ICTRP 등 기타 임상 레지스트리 추적.
* **🔔 Smart Notification:** 텔레그램 즉시 알림 및 이메일 모닝 브리핑.
* **🐳 Dockerized:** 시놀로지 NAS(Container Manager)에서 원클릭 배포 및 24시간 가동.

## 🛠️ Tech Stack (기술 스택)
* **Language:** Python 3.9
* **Infrastructure:** Docker, Docker Compose
* **Libraries:** `requests`, `feedparser`, `schedule`, `python-telegram-bot`
* **Environment:** Synology DSM 7.2+

## 🚀 Installation (설치 방법)

### 1. Clone Repository
\`\`\`bash
git clone https://github.com/YOUR_GITHUB_ID/Dr-AI-Sentinel.git
cd Dr-AI-Sentinel
\`\`\`

### 2. Configure Environment
\`src/.env.example\` 파일의 이름을 \`.env\`로 변경하고 설정을 입력하세요.
\`\`\`ini
TELEGRAM_TOKEN=your_token_here
CHAT_ID=your_chat_id
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
\`\`\`

### 3. Run with Docker
\`\`\`bash
docker compose up -d --build
\`\`\`

## 👨‍⚕️ Author
Developed by **Dr. Mingil** (Rehabilitation Medicine Specialist & Physician Engineer)


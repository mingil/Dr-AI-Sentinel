import os
import sys
from dotenv import load_dotenv

# 프로젝트 루트 경로 찾기
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')

# .env 로드
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    # 컨테이너 환경 등 예외 상황 대비
    load_dotenv()

# 경로 설정 (절대 경로로 변환)
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
LOG_FILE = os.path.join(LOG_DIR, 'system.log')

# 폴더 자동 생성 (안전장치)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# 환경변수 가져오기
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 리스트 변환 헬퍼 함수
def get_list(key):
    val = os.getenv(key, "")
    return [x.strip() for x in val.split(',') if x.strip()]

# 키워드 로드
KEYWORDS_JOURNAL = get_list("KEYWORDS_JOURNAL")
KEYWORDS_CLINICAL = get_list("KEYWORDS_CLINICAL")
KEYWORDS_TRIALS = get_list("KEYWORDS_TRIALS")

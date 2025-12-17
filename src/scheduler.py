import schedule
import time
import sys
import os
from datetime import datetime

# 프로젝트 루트 경로 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import logger, main

log = logger.get_logger("Scheduler")

def job():
    log.info("⏰ 예약된 시간이 되었습니다. 정기 업무를 시작합니다.")
    main.run_all_tasks()

if __name__ == "__main__":
    log.info("🚀 [닥터 AI] 24시간 대기 모드 가동 (매일 07:00 실행)")
    
    # 매일 아침 07:00에 실행 (Docker 시간대 설정 필수)
    schedule.every().day.at("07:00").do(job)
    
    # (옵션) 시작하자마자 테스트로 한 번 돌리고 싶으면 아래 주석 해제
    # job()

    while True:
        # 1분마다 할 일이 있는지 체크하고 잠듦
        schedule.run_pending()
        time.sleep(60)

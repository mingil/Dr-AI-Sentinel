import sys
import os
import time
import schedule
from datetime import datetime

# 프로젝트 루트 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src import config, logger
from bots import journal_bot, clinical_bot, trials_bot, dashboard, backup_bot

log = logger.get_logger("Master")

def job():
    log.info("📢 [닥터 AI] 정기 업무를 시작합니다...")
    start_time = time.time()

    tasks = [
        ("01.Journal", journal_bot.check_arm),
        ("01.Journal", journal_bot.check_apmr),
        ("03.Clinical", clinical_bot.check_trials),
        ("04.Trials", trials_bot.check_rss),
    ]

    for name, func in tasks:
        try:
            log.info(f"👉 [{name}] 실행 중...")
            func()
        except Exception as e:
            log.error(f"❌ [{name}] 오류: {e}")

    # 백업 및 리포트
    try:
        backup_bot.perform_backup()
        dashboard.send_report()
    except Exception as e:
        log.error(f"❌ 마무리 작업 오류: {e}")

    elapsed = time.time() - start_time
    log.info(f"🎉 업무 종료 (소요시간: {elapsed:.2f}초)")
    log.info("💤 다음 스케줄 대기 중...")

def run_scheduler():
    log.info("🚀 [닥터 AI] 24시간 감시 시스템 가동 시작")
    
    # [설정] 매일 아침 07:00 실행 (원하는 시간으로 변경 가능)
    schedule.every().day.at("07:00").do(job)
    
    # [테스트용] 개발 단계에서는 바로 한 번 실행해보고 싶다면 아래 주석 해제
#   job() 

    while True:
        schedule.run_pending()
        time.sleep(60) # 1분마다 시간 체크

if __name__ == "__main__":
    run_scheduler()

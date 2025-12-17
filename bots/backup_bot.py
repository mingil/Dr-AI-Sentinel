import sys
import os
import zipfile
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import config, logger

log = logger.get_logger("Backup")

def perform_backup():
    log.info("데이터 백업 시작...")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    zip_filename = os.path.join(config.BACKUP_DIR, f"backup_{timestamp}.zip")

    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 1. Data 폴더 백업
            for root, dirs, files in os.walk(config.DATA_DIR):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, arcname=f"data/{file}")
            
            # 2. Source Code 백업 (bots, src)
            for folder in ['src', 'bots']:
                target_dir = os.path.join(config.BASE_DIR, folder)
                for root, dirs, files in os.walk(target_dir):
                    for file in files:
                        if file.endswith('.py'):
                            file_path = os.path.join(root, file)
                            rel_path = os.path.relpath(file_path, config.BASE_DIR)
                            zipf.write(file_path, arcname=rel_path)

        size_kb = os.path.getsize(zip_filename) / 1024
        log.info(f"백업 완료: {zip_filename} ({size_kb:.1f} KB)")

    except Exception as e:
        log.error(f"백업 실패: {e}")

if __name__ == "__main__":
    perform_backup()

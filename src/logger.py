import logging
import sys
import os
from src import config

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        return logger

    # 포맷: [시간] [봇이름] 메시지
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # 1. 파일 핸들러 (logs/system.log에 저장)
    file_handler = logging.FileHandler(config.LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 2. 스트림 핸들러 (터미널 출력)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

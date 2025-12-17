import sys
import os
import feedparser
import ssl

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import config, logger, notifiers

# SSL 인증 우회
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

log = logger.get_logger("04.Trials")
SENT_LOG_FILE = os.path.join(config.DATA_DIR, "trials_sent.txt")
RSS_URL = "https://clinicaltrials.gov/ct2/results/rss.xml?rcv_d=14&lup_d=14&count=100"

def load_sent_list():
    if not os.path.exists(SENT_LOG_FILE): return []
    with open(SENT_LOG_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def save_sent_list(title):
    with open(SENT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(title + "\n")

def check_rss():
    log.info("임상시험(Trials) 감시 시작...")
    try:
        feed = feedparser.parse(RSS_URL)
        sent_list = load_sent_list()
        found_items = []
        
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            
            if any(k.lower() in title.lower() for k in config.KEYWORDS_TRIALS) and title not in sent_list:
                found_items.append(f"제목: {title}\n링크: {link}\n{'-'*30}")
                save_sent_list(title)
                log.info(f"신규 발견: {title[:30]}...")

        if found_items:
            subject = f"🧪 [Trials] 기초 임상 {len(found_items)}건 통합 보고"
            body = "\n".join(found_items)
            notifiers.send_email(subject, body)
            log.info(f"메일 발송 완료 ({len(found_items)}건)")
        else:
            log.info("신규 없음 (기존 기록 보유)")

    except Exception as e:
        log.error(f"Trials Error: {e}")

if __name__ == "__main__":
    check_rss()

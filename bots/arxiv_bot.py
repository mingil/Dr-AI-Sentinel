import sys
import os
import requests
import feedparser

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import config, logger, notifiers

log = logger.get_logger("02.ArXiv")
SENT_LOG_FILE = os.path.join(config.DATA_DIR, "arxiv_sent.txt")

# 검색어: (Rehabilitation OR Stroke) AND (Deep Learning OR AI)
SEARCH_QUERY = 'all:rehabilitation+AND+all:"deep+learning"'

def load_sent_list():
    if not os.path.exists(SENT_LOG_FILE): return []
    with open(SENT_LOG_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def save_sent_list(item_id):
    with open(SENT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(item_id + "\n")

def check_arxiv():
    log.info("ArXiv (AI/CS) 검색 중...")
    try:
        # ArXiv API 호출
        url = f'http://export.arxiv.org/api/query?search_query={SEARCH_QUERY}&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending'
        feed = feedparser.parse(url)
        
        found_items = []
        sent_list = load_sent_list()
        
        for entry in feed.entries:
            title = entry.title.replace('\n', ' ')
            link = entry.link
            doc_id = link.split('/')[-1] # URL 끝부분이 ID
            
            if doc_id not in sent_list:
                found_items.append(f"Title: {title}\nLink: {link}\n{'-'*30}")
                save_sent_list(doc_id)
                log.info(f"신규 발견: {title[:30]}...")

        if found_items:
            subject = f"🤖 [ArXiv] 미래기술/AI 신규 논문 {len(found_items)}건"
            body = "\n".join(found_items)
            notifiers.send_email(subject, body)
            log.info(f"메일 발송 완료 ({len(found_items)}건)")
        else:
            log.info("신규 없음 (기존 기록 보유)")

    except Exception as e:
        log.error(f"ArXiv Error: {e}")

if __name__ == "__main__":
    check_arxiv()

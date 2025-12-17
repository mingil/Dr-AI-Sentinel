import sys
import os
import requests
import feedparser

# [필수] 상위 폴더(src)를 인식하기 위한 경로 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import config, logger, notifiers

log = logger.get_logger("01.Journal")
SENT_LOG_FILE = os.path.join(config.DATA_DIR, "journal_sent.txt")
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def load_sent_list():
    if not os.path.exists(SENT_LOG_FILE): return []
    with open(SENT_LOG_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def save_sent_list(title):
    with open(SENT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(title + "\n")

def check_arm():
    log.info("ARM (PubMed) 검색 중...")
    try:
        url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
        params = {'db': 'pubmed', 'term': '"Ann Rehabil Med"[Journal]', 'retmode': 'json', 'retmax': '30', 'sort': 'date'}
        resp = requests.get(url, params=params, headers=HEADERS)
        ids = resp.json().get('esearchresult', {}).get('idlist', [])
        
        if not ids: return

        sum_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
        summaries = requests.get(sum_url, params={'db': 'pubmed', 'id': ','.join(ids), 'retmode': 'json'}, headers=HEADERS).json()
        
        sent_list = load_sent_list()
        found_items = []

        for uid in ids:
            item = summaries['result'][uid]
            title = item['title']
            # Config의 키워드 사용
            if any(k in title.lower() for k in config.KEYWORDS_JOURNAL) and title not in sent_list:
                link = f"https://pubmed.ncbi.nlm.nih.gov/{uid}/"
                
                # 텔레그램은 즉시 발송
                notifiers.send_telegram(f"🚨 [ARM 발견]\n{title}\n{link}")
                
                found_items.append(f"Title: {title}\nLink: {link}\n{'-'*30}")
                save_sent_list(title)
                log.info(f"발견: {title[:30]}...")

        if found_items:
            subject = f"📚 [ARM] 신규 논문 {len(found_items)}건 통합 보고"
            body = "\n".join(found_items)
            notifiers.send_email(subject, body)
            log.info(f"메일 발송 완료 ({len(found_items)}건)")

    except Exception as e:
        log.error(f"ARM Error: {e}")

def check_apmr():
    log.info("APMR (RSS) 검색 중...")
    try:
        feed = feedparser.parse("https://www.archives-pmr.org/inpress.rss")
        sent_list = load_sent_list()
        found_items = []
        
        for entry in feed.entries:
            title = entry.title
            full_text = (title + " " + getattr(entry, 'description', '')).lower()
            if any(k in full_text for k in config.KEYWORDS_JOURNAL) and title not in sent_list:
                notifiers.send_telegram(f"🚨 [APMR 발견]\n{title}\n{entry.link}")
                found_items.append(f"Title: {title}\nLink: {entry.link}\n{'-'*30}")
                save_sent_list(title)
                log.info(f"발견: {title[:30]}...")

        if found_items:
            subject = f"📚 [APMR] 신규 논문 {len(found_items)}건 통합 보고"
            body = "\n".join(found_items)
            notifiers.send_email(subject, body)
            log.info(f"메일 발송 완료 ({len(found_items)}건)")

    except Exception as e:
        log.error(f"APMR Error: {e}")

if __name__ == "__main__":
    check_arm()
    check_apmr()

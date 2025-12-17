import sys
import os
import requests
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import config, logger, notifiers

log = logger.get_logger("03.Clinical")
SENT_LOG_FILE = os.path.join(config.DATA_DIR, "clinical_sent.txt")

# [New] API v2 주소
BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; DrAI-Bot/1.0)'}

def load_sent_list():
    if not os.path.exists(SENT_LOG_FILE): return []
    with open(SENT_LOG_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def save_sent_list(item_id):
    with open(SENT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(item_id + "\n")

def check_trials():
    log.info("ClinicalTrials.gov (API v2) 검색 시작...")
    
    found_items = []
    sent_list = load_sent_list()
    
    for keyword in config.KEYWORDS_CLINICAL:
        try:
            # [API v2 파라미터]
            # query.term: 검색어
            # pageSize: 가져올 개수
            # sort: 최신순 정렬 (LastUpdateSubmitDate)
            params = {
                'query.term': keyword,
                'pageSize': 5,
                'sort': 'LastUpdateSubmitDate',
                'format': 'json'
            }
            
            resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=15)
            
            if resp.status_code != 200:
                log.error(f"API Error ({keyword}): Status Code {resp.status_code}")
                continue

            data = resp.json()
            # v2에서는 'studies' 키 안에 리스트가 들어있음
            studies = data.get('studies', [])

            if not studies:
                log.info(f"   검색 결과 없음: {keyword}")
                continue

            for study in studies:
                # v2 데이터 구조 파싱
                protocol = study.get('protocolSection', {})
                ident = protocol.get('identificationModule', {})
                
                nct_id = ident.get('nctId', 'Unknown')
                title = ident.get('officialTitle') or ident.get('briefTitle', 'No Title')
                
                if nct_id in sent_list: continue
                
                link = f"https://clinicaltrials.gov/study/{nct_id}"
                found_items.append(f"[{keyword}] {nct_id}\n제목: {title}\n링크: {link}\n{'-'*30}")
                save_sent_list(nct_id)
                log.info(f"신규 발견: {title[:30]}...")
                
            time.sleep(1) # API 예의 지키기
                
        except Exception as e:
            log.error(f"Error ({keyword}): {e}")

    if found_items:
        subject = f"💊 [Clinical] 신규 임상 {len(found_items)}건 통합 보고"
        body = "\n".join(found_items)
        notifiers.send_email(subject, body)
        log.info(f"메일 발송 완료 ({len(found_items)}건)")
    else:
        log.info("신규 없음 (기존 기록 보유)")

if __name__ == "__main__":
    check_trials()

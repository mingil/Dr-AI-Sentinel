import sys
import os
import requests

# 환경변수 로드
sys.path.append(os.getcwd())
from src import config

print("------------ [텔레그램 진단 시작] ------------")

# 1. 설정값 로드 확인 (비밀번호는 가리고 길이만 체크)
token = config.TELEGRAM_TOKEN
chat_id = config.CHAT_ID

if not token:
    print("❌ 에러: .env 파일에 TELEGRAM_TOKEN이 없습니다!")
else:
    print(f"✅ 토큰 로드됨 (길이: {len(token)})")

if not chat_id:
    print("❌ 에러: .env 파일에 CHAT_ID가 없습니다!")
else:
    print(f"✅ ID 로드됨: {chat_id}")

# 2. 실제 발송 테스트
if token and chat_id:
    print("🚀 메시지 발송 시도 중...")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(url, data={"chat_id": chat_id, "text": "🔔 [닥터 AI] 텔레그램 연결 테스트 성공!"})
        
        print(f"📡 응답 코드: {resp.status_code}")
        print(f"📄 응답 내용: {resp.text}")
        
        if resp.status_code == 200:
            print("🎉 결과: 성공! 핸드폰을 확인하세요.")
        else:
            print("🔥 결과: 실패! 위의 '응답 내용'을 닥터 AI에게 보여주세요.")
            
    except Exception as e:
        print(f"💥 치명적 오류: {e}")

print("---------------------------------------------")

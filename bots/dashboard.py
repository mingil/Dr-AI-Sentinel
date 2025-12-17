import sys
import os
import re
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import config, logger, notifiers

# 로거는 생성하되, 이 파일은 주로 읽기 전용이라 간단히 사용
log = logger.get_logger("Dashboard")

def analyze_logs():
    if not os.path.exists(config.LOG_FILE):
        return ["로그 파일이 없습니다."]

    # 로그에서 감지할 봇들의 서명 (logger.get_logger 이름과 매칭)
    bot_signatures = {
        "01.Journal": "01.Journal",
        "02.ArXiv": "02.ArXiv",  # (나중에 이식 예정)
        "03.Clinical": "03.Clinical",
        "04.Trials": "04.Trials",
        "05.Backup": "Backup",
    }
    
    with open(config.LOG_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # "정기 업무 시작" 최신 지점 찾기
    start_index = 0
    for i in range(len(lines) - 1, -1, -1):
        if "[Master Scheduler]" in lines[i]:
            start_index = i
            break
            
    today_logs = "".join(lines[start_index:])
    summary = []

    for name, sig in sorted(bot_signatures.items()):
        if f"[{sig}]" not in today_logs:
            summary.append(f"{name:<15} | 💤 대기 중")
            continue
            
        # 해당 봇의 로그 섹션만 추출 (단순화: 해당 시그니처가 있는 줄들 분석)
        bot_lines = [l for l in lines[start_index:] if f"[{sig}]" in l]
        bot_text = "".join(bot_lines)
        
        status = "🔄 실행됨"
        if "메일 발송 완료" in bot_text:
            match = re.search(r'메일 발송 완료 \((\d+)건\)', bot_text)
            cnt = match.group(1) if match else "?"
            status = f"🚀 {cnt}건 발견"
        elif "신규 없음" in bot_text:
            status = "✅ 신규 없음"
        elif "백업 완료" in bot_text:
            status = "💾 백업 완료"
        elif "Error" in bot_text:
            status = "⚠️ 에러 발생"
            
        summary.append(f"{name:<15} | {status}")

    return summary

def send_report():
    today = datetime.now().strftime("%Y-%m-%d")
    summary_lines = analyze_logs()
    
    body_lines = [
        f"🏥 [닥터 AI] Dr-AI-Pro 아침 브리핑 ({today})",
        "="*40,
        "봇(Bot) 이름      | 실행 결과",
        "-"*40
    ] + summary_lines + [
        "-"*40,
        f"📂 로그 위치: {config.LOG_FILE}",
        f"📂 데이터 위치: {config.DATA_DIR}"
    ]
    
    report_text = "\n".join(body_lines)
    
    # 이메일 발송 (화면 출력은 master_scheduler에서 처리)
    notifiers.send_email(f"☀️ [Morning Brief] 통합 보고 ({today})", report_text)
    print(report_text)

if __name__ == "__main__":
    send_report()

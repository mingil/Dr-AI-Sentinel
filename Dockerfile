# 1. 가벼운 파이썬 3.9 이미지 사용
FROM python:3.9-slim

# 2. 작업 폴더 설정
WORKDIR /app

# 3. 시간대 설정 (한국 시간 KST)
# 이게 없으면 봇이 영국 시간(UTC) 기준으로 아침 7시에 일어납니다.
RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# 4. 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 소스 코드 복사
COPY . .

# 6. 실행 명령어
CMD ["python", "src/main.py"]

# docker run -d tg-bot-yt-download:0.0.1
# docker run -d -v `pwd`:/app tg-bot-yt-download:0.0.1
FROM thecanadianroot/opencv-cuda:pr-8-12.0.0-base-ubuntu22.04

WORKDIR /app
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev build-essential ffmpeg


COPY requirements.txt /app/
COPY *.py /app/
COPY .env /app/

RUN pip3 install --no-cache-dir -r requirements.txt


ENTRYPOINT ["tail", "-f", "/dev/null"]
# CMD ["python3", "bot.py"]

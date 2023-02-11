# docker run -d tg-bot-yt-download:0.0.1
FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev build-essential


COPY requirements.txt /app/
COPY bot.py /app/
COPY .env /app/

RUN pip3 install --no-cache-dir -r requirements.txt


# ENTRYPOINT ["tail", "-f", "/dev/null"]
CMD ["python3", "bot.py"]

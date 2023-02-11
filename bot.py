import requests
import telebot
import logging
import os
from pytube import YouTube
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

def download_video(url):
    yt = YouTube("https://www.youtube.com/watch?v=-vrnlAX7w2A")
    return yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()    


@bot.message_handler(commands=['download'])
def handle_download(message):
    if len(message.text.split()) == 2:
        url = message.text.split()[1]
        vid_path = download_video(url)
        bot.send_document(chat_id=message.chat.id, document=open(vid_path, 'rb'))
        os.remove(vid_path)
    else:
        bot.send_message(chat_id=message.chat.id, text='Invalid format. Use /download <video_url> to download a video.')

bot.polling()
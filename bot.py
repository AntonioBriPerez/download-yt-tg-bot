import requests
import telebot
from telebot.types import Message
import logging
import os
from pytube import YouTube
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Starting up bot...")
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
logging.info("Bot is up and running!")
def download_video(url):
    try:
        yt = YouTube(url)
        return yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()    
    except Exception as e: 
        logging.error(f"Ha habido un error: {e}")


def print_message_metadata(message: Message):
    logging.info(f'Message recieved: {message.text}')
    logging.info(f"Date: {message.date}")
    logging.info(f"Sender first name: {message.from_user.first_name}")
    logging.info(f"Sender last name: {message.from_user.last_name}")
    logging.info(f"Sender username: {message.from_user.username}")



@bot.message_handler(commands=['download'])
def handle_download(message):
    if len(message.text.split()) == 2:
        url = message.text.split()[1]
        print_message_metadata(message)
        
        if vid_path := download_video(url):
            logging.info(f"Path del video: {vid_path}")
            bot.send_document(chat_id=message.chat.id, document=open(vid_path, 'rb'))
    else:
        bot.send_message(chat_id=message.chat.id, text='Invalid format. Use /download <video_url> to download a video.')

bot.polling()
import requests
import telebot
from telebot.types import Message
import logging
import os
from pytube import YouTube
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

def download_video(url):
    try:
        yt = YouTube(url)
        return yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()    
    except Exception as e: 
        logging.error(f"Ha habido un error: {e}")


def download_video_audio(url): 
    try:
        yt = YouTube(url)
        return yt.streams.filter(only_audio=True).first().download()
    except Exception as e: 
        logging.error(f"Ha habido un error: {e}")
        
def print_message_metadata(message: Message):
    logging.info(f'Message recieved: {message.text}')
    logging.info(f"Date: {message.date}")
    logging.info(f"Sender first name: {message.from_user.first_name}")
    logging.info(f"Sender last name: {message.from_user.last_name}")
    logging.info(f"Sender username: {message.from_user.username}")

@bot.message_handler(commands=['start'])
def start(message):
    print(print_message_metadata(message))
    logging.info("Starting up bot...")
    bot.send_message(chat_id=message.chat.id, text='Hello motherfucker!!! You wanna some yee yee ass videos or audios?')
    logging.info("Bot is up and running!")


@bot.message_handler(commands=['download'])
def handle_download(message):
    if len(message.text.split()) == 2:
        url = message.text.split()[1]
        print_message_metadata(message)
        
        if vid_path := download_video(url):
            logging.info(f"Path del video: {vid_path}")
            bot.send_document(chat_id=message.chat.id, document=open(vid_path, 'rb'))
            os.remove(vid_path)
    else:
        bot.send_message(chat_id=message.chat.id, text='Invalid format. Use /download <video_url> to download a video.')

@bot.message_handler(commands=['download_audio'])
def handle_download_audio(message):
    if len(message.text.split()) == 2:
        url = message.text.split()[1]
        print_message_metadata(message)
        
        if vid_path := download_video_audio(url):
            logging.info(f"Path del video: {vid_path}")
            ext = os.path.splitext(vid_path)[1]
            new_name = vid_path.replace(ext, '.mp3')
            os.rename(vid_path, new_name)
            bot.send_document(chat_id=message.chat.id, document=open(new_name, 'rb'))
            os.remove(new_name)
    else:
        bot.send_message(chat_id=message.chat.id, text='Invalid format. Use /download_audio <video_url> to download the audio of a video.')

@bot.message_handler(commands=['help'])
def handle_help(message): 
    bot.send_message(chat_id=message.chat.id, text='This is what I can do: \n /download <video_url> to download a video. \n /download_audio <video_url> to download the audio of a video.')

    
bot.polling()

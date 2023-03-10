import telebot
from telebot.types import Message
import logging
import os
from dotenv import load_dotenv
from video_utils import split_video, download_asset, get_file_size
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

def print_message_metadata(message: Message):
    logger.info(f'Message recieved: {message.text}')
    logger.info(f"Sender first name: {message.from_user.first_name}")
    logger.info(f"Sender last name: {message.from_user.last_name}")
    logger.info(f"Sender username: {message.from_user.username}")

@bot.message_handler(commands=['start'])
def start(message):
    print(print_message_metadata(message))
    logger.info("Starting up bot...")
    bot.send_message(chat_id=message.chat.id, text='Hello motherfucker!!! You wanna some yee yee ass videos or audios? \
    Type /help to check what I can do.')
    logger.info("Bot is up and running!")

@bot.message_handler(commands=['health'])
def handle_health(message):
    bot.send_message(chat_id=message.chat.id, text='up and running!')


@bot.message_handler(commands=['download'])
def handle_download(message):
    handle_asset(message, bot)
    

def handle_asset(message, bot, audio=False):
    if len(message.text.split()) == 2:
        url = message.text.split()[1]
        print_message_metadata(message)
        if audio:
            if vid_path := download_asset(url, message, bot, audio=True):
                handle_audio(message, bot, vid_path)
        else:
            if vid_path := download_asset(url, message, bot):
                handle_video(message, bot, vid_path)
                
    else:
        bot.send_message(chat_id=message.chat.id, text='Invalid format. Use /download <video_url> to download a video.')

def handle_video(message, bot, vid_path):
    video_size = get_file_size(vid_path)
    bot.send_message(text="Video size: " + str(video_size) + " MB", chat_id=message.chat.id)
    split_video(vid_path, bot, message, parts_size_mb=50)

def handle_audio(message, bot, vid_path):
    ext = os.path.splitext(vid_path)[1]
    new_name = vid_path.replace(ext, '.mp3')
    os.rename(vid_path, new_name)
    bot.send_document(chat_id=message.chat.id, document=open(new_name, 'rb'))
    os.remove(new_name)
            


@bot.message_handler(commands=['download_audio'])
def handle_download_audio(message):
    handle_asset(message, bot, audio=True)


@bot.message_handler(commands=['help'])
def handle_help(message): 
    bot.send_message(chat_id=message.chat.id, text='This is what I can do: \n /download <video_url> (MAXIMUM VIDEO SIZE IS 50MB, if not it will be splitted!) to download a video. \n /download_audio <video_url> to download the audio of a video.')

    
bot.polling()

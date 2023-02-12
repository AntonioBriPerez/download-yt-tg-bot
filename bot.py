import telebot
from telebot.types import Message
import logging
import os
from dotenv import load_dotenv
from video_utils import deliver_video, download_video, download_video_audio
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

def get_file_size(file_path):
    file_size = os.path.getsize(file_path)
    return file_size / (1024 * 1024)

@bot.message_handler(commands=['download'])
def handle_download(message):
    if len(message.text.split()) == 2:
        url = message.text.split()[1]
        print_message_metadata(message)
        logger.info("Downloading video...")
        if vid_path := download_video(url, message, bot):
            logger.info(f"Path del video: {vid_path}")
            video_size = get_file_size(vid_path)
            logger.info("Total video size: " + str(video_size) + " MB")
            bot.send_message(text="Video size: " + str(video_size) + " MB", chat_id=message.chat.id)
            if video_size >= 45:
                bot.send_message(text="Videos over 45 MB are not supported. Processing in chunks of 45MB aproximately... (it can be slow 10-15 minutes)", chat_id=message.chat.id)
                deliver_video(vid_path, bot,message,max_size_mb=45)
            else:
                bot.send_document(chat_id=message.chat.id, document=open(vid_path, 'rb'))
                logger.info("Video sent successfully")
            os.remove(vid_path)
    else:
        bot.send_message(chat_id=message.chat.id, text='Invalid format. Use /download <video_url> to download a video.')

@bot.message_handler(commands=['download_audio'])
def handle_download_audio(message):
    if len(message.text.split()) == 2:
        url = message.text.split()[1]
        print_message_metadata(message)
        
        if vid_path := download_video_audio(url, message, bot):
            logger.info(f"Path del video: {vid_path}")
            ext = os.path.splitext(vid_path)[1]
            new_name = vid_path.replace(ext, '.mp3')
            os.rename(vid_path, new_name)
            bot.send_document(chat_id=message.chat.id, document=open(new_name, 'rb'))
            os.remove(new_name)
    else:
        bot.send_message(chat_id=message.chat.id, text='Invalid format. Use /download_audio <video_url> to download the audio of a video.')

@bot.message_handler(commands=['help'])
def handle_help(message): 
    bot.send_message(chat_id=message.chat.id, text='This is what I can do: \n /download <video_url> (MAXIMUM VIDEO SIZE IS 50MB, if not it will be splitted!) to download a video. \n /download_audio <video_url> to download the audio of a video.')

    
bot.polling()

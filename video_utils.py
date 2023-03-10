import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube
from uuid import uuid4
import logging
logger = logging.getLogger(__name__)

def get_file_size(file_path):
    file_size = os.path.getsize(file_path)
    return file_size / (1024 * 1024)


def download_asset(url, message, bot, audio=False): 
    try:
        yt = YouTube(url)
        if not audio: 
            return yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution().download(filename=f"video_{str(uuid4())}.mp4")
        else: 
            return yt.streams.filter(only_audio=True).first().download() 
                
    except Exception as e: 
        logger.error(f"Ha habido un error: {e}")
        bot.send_message(chat_id=message.chat.id, text='There was an error downloading the video')    


def split_video(file_path, bot,message,parts_size_mb=40):
    # Load the video file using moviepy
    video = VideoFileClip(file_path)

    # Calculate the length of the video in seconds
    video_length = video.duration

    # Calculate the size of the video file in MB
    file_size = os.path.getsize(file_path) / 1048576
    if file_size <= parts_size_mb:
        # If the file is smaller than the maximum size, return the file as a single part
        bot.send_video(chat_id=message.chat.id, video=open(file_path, 'rb'))
        os.remove(file_path)
    
    else:
        # Calculate the number of parts
        num_parts = int(file_size / parts_size_mb) + 1

        # Calculate the duration of each part
        part_duration = video_length / num_parts

        # Split the video into parts and return a list of part paths
        part_paths = []
        for i in range(num_parts):
            bot.send_message(chat_id=message.chat.id, text=f"Processing video {i+1}/{num_parts}")
            part_start = i * part_duration
            part_end = (i + 1) * part_duration
            part_video = video.subclip(part_start, part_end)
            filename, extension = os.path.splitext(file_path)
            part_path = f'{filename}_part{i}{extension}'
            part_paths.append(part_path)
            part_video.write_videofile(part_path)
            bot.send_video(chat_id=message.chat.id, video=open(part_path, 'rb'))
            os.remove(part_path)

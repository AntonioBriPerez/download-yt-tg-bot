import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import logging
from pytube import YouTube
from uuid import uuid4
import cv2
logger = logging.getLogger(__name__)

def download_video_audio(url, message, bot): 
    try:
        yt = YouTube(url)
        return yt.streams.filter(only_audio=True).first().download()
    except Exception as e: 
        logger.error(f"Ha habido un error: {e}")
        bot.send_message(chat_id=message.chat.id, text='There was an error downloading the audio')


def download_video(url, message, bot):
    try:
        yt = YouTube(url)
        return yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution().download(filename=f"video_{str(uuid4())}.mp4")    
    except Exception as e: 
        logger.error(f"Ha habido un error: {e}")
        bot.send_message(chat_id=message.chat.id, text='There was an error downloading the video')

def deliver_video(file_path, bot,message,max_size_mb=50):
    cap = cv2.VideoCapture(file_path)
    chunk_size = max_size_mb * 1024 * 1024  # Convert MB to bytes

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Set the FourCC code to use for the output files
    video_info = {
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    }

    chunk_num = 1
    chunk_size_frames = int(chunk_size / video_info["fps"] / (video_info["width"] * video_info["height"] * 3))
    out = None
    frame_count = 0
    while True:
        bot.send_message(chat_id=message.chat.id, text=f"Processing part {chunk_num} of the video")
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % chunk_size_frames == 0:
            if out is not None:
                out.release()
            out = cv2.VideoWriter(os.path.join(os.getcwd(), f"{os.path.splitext(os.path.basename(file_path))[0]}_part{chunk_num}.mp4"),
                                  fourcc, video_info["fps"], (video_info["width"], video_info["height"]), isColor=True)
            chunk_num += 1

        out.write(frame)
        bot.send_document(chat_id=message.chat.id, document=open(os.path.join(os.getcwd(), f"{os.path.splitext(os.path.basename(file_path))[0]}_part{chunk_num}.mp4"), 'rb'))
        frame_count += 1

    cap.release()
    if out is not None:
        out.release()
    logger.info("All parts sent successfully!")
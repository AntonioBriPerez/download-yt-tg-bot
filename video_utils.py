import ffmpeg
import os
import logging
from moviepy.video.io.VideoFileClip import VideoFileClip
def split_video(file_path, max_size_mb=50):
    # Load the video file using moviepy
    video = VideoFileClip(file_path)

    # Calculate the length of the video in seconds
    video_length = video.duration

    # Calculate the size of the video file in MB
    file_size = os.path.getsize(file_path) / 1048576
    if file_size <= max_size_mb:
        # If the file is smaller than the maximum size, return the file as a single part
        return [file_path]

    # Calculate the number of parts
    num_parts = int(file_size / max_size_mb) + 1

    # Calculate the duration of each part
    part_duration = video_length / num_parts

    # Split the video into parts and return a list of part paths
    part_paths = []
    for i in range(num_parts):
        part_start = i * part_duration
        part_end = (i + 1) * part_duration
        part_video = video.subclip(part_start, part_end)
        filename, extension = os.path.splitext(file_path)
        part_path = f'{filename}_part{i}{extension}'
        part_paths.append(part_path)
        part_video.write_videofile(part_path)

    return part_paths
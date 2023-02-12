import ffmpeg
import os
import logging

def split_video(file_path, max_size_mb=50):
    # Calculate the size of the video file in MB
    file_size = os.path.getsize(file_path) / 1048576
    if file_size <= max_size_mb:
        # If the file is smaller than the maximum size, return the file as a single part
        return [file_path]

    # Calculate the number of parts
    num_parts = int(file_size / max_size_mb) + 1

    # Calculate the size of each part in bytes
    part_size = int(file_size * 1048576 / num_parts)

    with open(file_path, 'rb') as f:
        # Split the file into parts and return a list of part paths
        part_paths = []
        for i in range(num_parts):
            filename, extension = os.path.splitext(file_path)
            part_path = f'{filename}_part{i}{extension}'
            part_paths.append(part_path)
            with open(part_path, 'wb') as part:
                part.write(f.read(part_size))

    return part_paths
 

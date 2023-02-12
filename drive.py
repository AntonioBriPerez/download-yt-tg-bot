from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def upload_video_to_drive(file_path):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    file = drive.CreateFile()
    file.SetContentFile(file_path)
    file.Upload()

upload_video_to_drive('./README.md')
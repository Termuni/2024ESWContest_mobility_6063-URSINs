
import os
import subprocess

mp3_process = None
def Play_MP3(mp3_name):
    global mp3_process
    Stop_MP3()
    mp3_process = subprocess.Popen(['mpg321', mp3_name])
        
def Stop_MP3():
    global mp3_process
    if mp3_process is not None:
        mp3_process.terminate()
        mp3_process = None
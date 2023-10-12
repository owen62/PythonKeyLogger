from cryptography.fernet import Fernet
import sys

def save_key():
    try:
        # Generate key
        key = Fernet.generate_key()
        
        # Save key to file
        with open("keyfile.key", 'wb') as f:
            f.write(key)

        print("Key saved to keyfile.key.")

    except Exception as e:
        print(f"An error occurred while saving the key: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    save_key()

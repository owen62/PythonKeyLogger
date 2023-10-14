from cryptography.fernet import Fernet
import logging
import os

# Constants for file paths
clipencrypted = "clipboard.txt"
keylogencrypted = "keylogfile.txt"

def decrypt(file_path):
    try:
        with open("keyfile.key", "rb") as filekey:
            key = filekey.read()

        # Load the content of the file
        with open(file_path, 'rb') as inputfile:
            encrypted = inputfile.read()

        # Decrypt the content
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted)

        # Get the file name without extension
        base_file_name = os.path.splitext(file_path)[0]

        # Write the decrypted content to a new file
        decrypted_file_path = f"{base_file_name}_decrypted.txt"
        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted)

        return decrypted_file_path
    except Exception as e:
        logging.error(f"An error occurred during decryption: {str(e)}")

def main():
    try:
        # Decrypt the LOG_FILE and CLIPBOARD
        decrypted_log_file = decrypt(keylogencrypted)
        decrypted_clipboard = decrypt(clipencrypted)

        if decrypted_log_file and decrypted_clipboard:
            # Print the paths of decrypted files
            print("Decrypted LOG_FILE:", decrypted_log_file)
            print("Decrypted CLIPBOARD:", decrypted_clipboard)
        else:
            print("Decryption failed for one or more files.")

    except Exception as e:
        logging.exception(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("Control-C entered...Program exiting ")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
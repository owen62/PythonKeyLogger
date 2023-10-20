from cryptography.fernet import Fernet

ZIP ='test.zip'

def decryptzip(zipe_file_path):
    with open('keyfile.key', 'rb') as keyfile:
        key = keyfile.read()
    fernet = Fernet(key)
    
    with open(zipe_file_path, 'rb') as encrypted_zip:
        zip_data = encrypted_zip.read()

    decrypted_zip_data = fernet.decrypt(zip_data)

    with open(zipe_file_path, 'wb') as decrypted_zip:
        decrypted_zip.write(decrypted_zip_data)


if __name__ == "__main__":
    decryptzip(ZIP)
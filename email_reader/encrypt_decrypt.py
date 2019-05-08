import os
from math import sqrt
from collections import defaultdict
from cryptography.fernet import Fernet


def get_abs_path(path):
    return os.path.join(os.path.dirname(__file__), path)

encryption_key_path = get_abs_path('encryption_key.txt')

class EncryptDecrypt(object):


    def encrypt_data(self, userName, password):
        
        key = self.get_encription_key()

        cipher_suite = Fernet(key)
        userName = cipher_suite.encrypt(bytes(userName,encoding='utf8'))
        print("\nUserName    : "+str(userName))

        password = cipher_suite.encrypt(bytes(password,encoding='utf8'))
        print("\nPassword    : "+str(password))

    def decrypt_data(self, encrypt_input):

        key = self.get_encription_key()
        cipher_suite = Fernet(key)
        decoded_text = cipher_suite.decrypt(encrypt_input)
        return decoded_text.decode("utf-8")

    def get_encription_key(self):
        key_file_path = os.path.isfile(encryption_key_path)
        if key_file_path:

            with open(encryption_key_path, 'rb') as keyFile:
                password_key =  keyFile.read()

        else :
            key = Fernet.generate_key() 
            with open(encryption_key_path, 'wb') as keyFile:
                keyFile.write(key)
                password_key = key

        return password_key


    def encrypted(self,text):
        scores = defaultdict(lambda: 0)
        for letter in text: scores[letter] += 1
        largest = max(scores.values())
        average = len(text) / 50.0
        return largest < average + 5 * sqrt(average)
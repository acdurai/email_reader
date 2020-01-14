from email_reader.encrypt_decrypt import EncryptDecrypt

def test_encryption():
    ed = EncryptDecrypt()
    ed.encrypt_data("pytest@gmail.com","pytest@123")

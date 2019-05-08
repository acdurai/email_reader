import time
import email
import imaplib
import smtplib
from itertools import chain
from email_reader.encrypt_decrypt import EncryptDecrypt




class ReadEmail(object):

    def __init__(self, username, password,email_folder="INBOX",email_type="UNSEEN", from_adr=None,subject=None,body=None):

        ed = EncryptDecrypt()
        self.username = ed.decrypt_data(username)if ed.encrypted(username) else username
        self.password = ed.decrypt_data(password)if ed.encrypted(password) else password
        self.from_adr = from_adr
        self.subject = subject
        self.email_folder = email_folder
        self.email_type = email_type
        self.body = body

    def search_criteria(self):
        search_dict = {}
        if self.from_adr:
            search_dict.update(FROM=self.from_adr)
        if self.subject:
            search_dict.update(SUBJECT=self.subject)
        if self.body:
            search_dict.update(BODY=self.body)
        return search_dict


    def search_string(self):
        criteria = self.search_criteria()
        c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items()))
        return '(%s)' % ' '.join(chain(*c))

    def get_email_body_content(self,email_content):
        if email_content.is_multipart():

            for payload in email_content.get_payload():
                cont_type = payload.get_content_type()

                if cont_type == "text/html":
                    email_content = payload.get_payload(decode=True)
                else :
                    email_content = payload.get_payload()
        else :
            cont_type = email_content.get_content_type()
            if cont_type == "text/html":
                email_content = email_content.get_payload(decode=True)
            else :
                email_content = email_content.get_payload()
        return email_content.decode('utf-8')

    def get_all_email_content(self,email_imap,email_list):
        dict_list=[]
        for e_id in email_list:
            data_dict = {}
            result, data = email_imap.uid('fetch', e_id, '(RFC822)')
            email_message = email.message_from_bytes(data[0][1])
            data_dict.update(mail_to = email_message['To'])
            data_dict.update(mail_subject = email_message['Subject'])
            data_dict.update(mail_from = email.utils.parseaddr(email_message['From']))
            data_dict.update(body = self.get_email_body_content(email_message))
            dict_list.append(data_dict)
        return dict_list

    def get_specific_email_content(self,email_imap,email_list,validationdata):
        dict_list=[]
        print(len(email_list))
        for e_id in email_list:
            data_dict = {}
            result, data = email_imap.uid('fetch', e_id, '(RFC822)')
            email_message = email.message_from_bytes(data[0][1])
            body_content = self.get_email_body_content(email_message)
            if validationdata in str(body_content):
                data_dict.update(mail_to = email_message['To'])
                data_dict.update(mail_subject = email_message['Subject'])
                data_dict.update(mail_from = email.utils.parseaddr(email_message['From']))
                data_dict.update(body = self.get_email_body_content(email_message))
                dict_list.append(data_dict)
        return dict_list

    def login_to_gmail(self):
        SMTP_SERVER = "imap.gmail.com"
        SMTP_PORT   = 993
       
        try:
            imap = imaplib.IMAP4_SSL(SMTP_SERVER)
            imap.login(self.username,self.password)
            print("\nGmail login success\n")
            
        except Exception as e:
            raise Exception(e)

        return imap

    def search_email(self,email_imap):
        
        email_imap.select(self.email_folder)
        if self.search_criteria():
            status, response = email_imap.uid('search', None, self.email_type, self.search_string())
        else:
            status, response = email_imap.uid('search', None, self.email_type)
        if status == 'OK':
            unread_msg = response[0].split()
        else:
            unread_msg = []

        return unread_msg

    def parse_all_email(self):
        n = 120
        email_imap = self.login_to_gmail()
        print("Waiting to receive email")
        for i in range(n):
            message_list = self.search_email(email_imap )
            email_content = self.get_all_email_content(email_imap,message_list)
            if len(email_content) != 0:
                break
            elif (i == n-1):
                raise Exception("Email is not recieved")
            time.sleep(1)
        email_imap.logout()
        return email_content

    def parse_specific_email(self,validationdata):
        n=120
        email_imap = self.login_to_gmail()
        print("Waiting to receive email")
        for i in range(n):
            message_list = self.search_email(email_imap )
            email_content = self.get_specific_email_content(email_imap,message_list,validationdata)
            if len(email_content) != 0:
                    break
            elif (i == n-1):
                raise Exception(f"Email is not recieved with this validation data : {validationdata}")
            time.sleep(1)
        email_imap.logout()
        return email_content[0]

        



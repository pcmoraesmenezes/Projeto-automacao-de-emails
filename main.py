import os
from pathlib import Path
from dotenv import load_dotenv
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import subprocess
from selenium .common.exceptions import TimeoutException

CAMINHO_MENSAGEM = Path(__file__).parent / 'mensagem.txt'

def enviar_email():
    load_dotenv()
    remetente = os.getenv('FROM_EMAIL', '')
    destinatario = remetente
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smpt_user = os.getenv('FROM_EMAIL', '')
    smtp_password = os.getenv('SENHA_EMAIL', '')

    with open(CAMINHO_MENSAGEM, 'r') as file:
        arquivo = file.read()
        template = Template(arquivo)
        texto = template.substitute(nome="Paulo")
    
    mime_multipart = MIMEMultipart()
    mime_multipart['from'] = remetente
    mime_multipart['to'] = destinatario
    mime_multipart['subject'] = "TESTANDO"

    corpo_email = MIMEText(texto, 'plain', 'utf-8')
    mime_multipart.attach(corpo_email)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(smpt_user, smtp_password)
        server.send_message(mime_multipart)
        print('Email enviado com sucesso')

CAMINHO_ENV = Path(__file__).parent / '.env'
ROOT_FOLDER = Path(__file__).parent
CHROME_DRIVER_EXE = ROOT_FOLDER / 'driver' / 'chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_services = webdriver.chrome.service.Service(executable_path=CHROME_DRIVER_EXE)
chrome_browser = webdriver.Chrome(service=chrome_services, options=chrome_options)

def caminho_email():
    if os.path.isfile(CAMINHO_ENV):
        load_dotenv()
        LOGIN = os.getenv('LOGIN')
        SENHA = os.getenv('SENHA')
    else:
        print('Arquivo .env não encontrado')
        return
    try:
        # Abre a página de login do Gmail
        chrome_browser.get('https://accounts.google.com/v3/signin/identifier?dsh=S-1123588098%3A1690459661043675&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ifkv=AeDOFXhVE1IFRojL6avwC9M5fC8ZsPojtAW5phfesRg5s9FqrvbZh3Yq14LAK5iYpRUv9e3Uk1ss&rip=1&sacu=1&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin')

        # Realiza o login
        logar = WebDriverWait(chrome_browser, 10).until(EC.presence_of_element_located((By.ID, 'identifierId')))
        logar.send_keys(LOGIN)
        logar.send_keys(Keys.ENTER)

        time.sleep(3)

        colocar_senha = WebDriverWait(chrome_browser, 10).until(EC.presence_of_element_located((By.NAME, 'Passwd')))
        colocar_senha.send_keys(SENHA)
        colocar_senha.send_keys(Keys.ENTER)
        time.sleep(30)
    except:
        print('Erro')
caminho_email()



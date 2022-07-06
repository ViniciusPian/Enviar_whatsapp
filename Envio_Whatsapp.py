import pandas as pd

contatos_df = pd.read_excel("Enviar.xlsx")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib.request import urlopen, URLError
from selenium.common.exceptions import TimeoutException

import validators
import time
import timeit
import urllib
import phonenumbers

cont = 0
cont1 = 0
lista_de_erros=[]
inicio = time.time()
hora = timeit.default_timer()

def validate_web_url(url):
    try:
        urlopen(url)
        return True
    except URLError:
        return False

def gravar_erro(nome: str, telefone: str):
    lista_de_erros.append((nome,telefone))
    with open('log_erros.txt','a') as arquivos:
        arquivos.writelines(f'{nome},{telefone} \n')

def gravar_envio(nome: str, telefone: str):
    with open('enviados.txt','a') as arquivos:
        arquivos.writelines(f'{nome},{telefone} \n')

navegador = webdriver.Chrome()  # webdriver.Firefox()
navegador.get("https://web.whatsapp.com/")
navegador.maximize_window()

while len(navegador.find_elements(By.ID, "side")) < 1:
    time.sleep(1)

# já estamos com o login feito no whatsapp web

for i, mensagem in enumerate(contatos_df['Mensagem']):
     pessoa = contatos_df.loc[i, "Pessoa"]
     numero = contatos_df.loc[i, "Número"]
     texto = urllib.parse.quote(f"Prezado(a) {pessoa}, {mensagem}")
     link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
     tel_num = str(numero)
     phone_number = phonenumbers.parse(tel_num,"BR")
#try:
     # if validate_web_url(link):
     navegador.get(link)
     #else:
     #   gravar_erro(pessoa, numero)
     #   continue
     #if phonenumbers.is_valid_number(phone_number):
     #   navegador.get(link)
     #else:
     #    gravar_erro(pessoa, numero)
     #    continue
#except selenium.common.exceptions.UnexpectedAlertPresentException:
#     Pass
     gravar_envio(pessoa, numero)
     while len(navegador.find_elements(By.ID, "side")) < 1:
      time.sleep(1)
      time.sleep(20)
      cont = cont + 1
     #navegador.find_element(By.XPATH,'/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]').send_keys(Keys.ENTER)
try:
     element_present = WebDriverWait(navegador, 30).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')))
     element_present.send_keys(Keys.ENTER)
     gravar_envio(pessoa, numero)
     time.sleep(1)
     cont1=cont1+1
except TimeoutException:
     gravar_erro(pessoa, numero)
     pass
fim = time.time()
horaf = timeit.default_timer()
tempo = (fim-inicio)/60
with open('time.txt','a') as arquivo:
    arquivo.writelines(f'hora inicio: {hora}\n')
    arquivo.writelines(f'hora fim: {horaf}\n')
    arquivo.writelines(f'tempo de execução: {(horaf-hora):.2f} seg, Mensagens enviadas:{cont} {cont1} \n')
#   for indice, dados in enumerate(lista_de_erros, start=0):
#   nome, telefone = dados

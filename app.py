#importando as bibliotecas nescessarias 
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from datetime import datetime

site_noticias = "https://www.uol.com.br"

#buscando o conteudo do site em html 
options = Options()
options.add_argument('--headless')
options.add_argument('window-size=400,800')
service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service, options=options)
navegador.get(site_noticias)
# sleep(2)
site = BeautifulSoup(navegador.page_source, "html.parser")

#Escrevendo o arquivo coletado em txt 
arquivo = open("noticias.txt", "w")

# #pegando a manchete do site 
manchete = site.find(class_='headlineMain__title')
manchete_noticia = f"Manchete principal: {manchete.get_text().strip()}"

arquivo.write(f"{manchete_noticia}\n")
arquivo.write("--------------------------------------------------------------------------------------------------\n")

#pegando o top 5 noticias do site 
arquivo.write("TOP 5 NOTICIAS!\n")
lista_noticias = site.find_all("h3",class_="title__element headlineSub__content__title")
contador = 1
for noticia in lista_noticias:
    if contador <= 5:
        arquivo.write(f"Noticia: {noticia.get_text().strip()}\n")
        contador = contador+1
    else: 
        break    
arquivo.write("--------------------------------------------------------------------------------------------------\n\n")

#iniciando a coleta de esportes 
section_esportes = site.find('section', attrs={'data-key' : "esporte"})
esportes_container = section_esportes.find("article", class_="headlineMain section__grid__main__highlight__item")

#pegando a manchete de esportes 
manchete_esporte = esportes_container.find("h3", class_="title__element headlineMain__title")
manchete_noticia_esporte = f"Manchete principal: {manchete_esporte.get_text().strip()}"

#pegando o top 5 noticias sobre esportes 
arquivo.write("TOP 5 NOTICIAS SOBRE ESPORTES!\n")

arquivo.write(f"{manchete_noticia_esporte}\n")
arquivo.write("--------------------------------------------------------------------------------------------------\n")
section_grid_main_rows = section_esportes.find(class_="section__grid__main__rows")
section_grid = section_grid_main_rows.find(class_="sectionGrid")
lista_not_esportes = section_grid.find_all("h3", class_="title__element headlineSub__content__title")
 
contador = 1
for not_esportes in lista_not_esportes:        
    arquivo.write(f"Noticia: {not_esportes.get_text().strip()}\n")
    contador = contador+1
    
arquivo.write("--------------------------------------------------------------------------------------------------\n")

arquivo.write(f"Fonte: {site_noticias} - Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
arquivo.close()

print("Extração finalizada.")

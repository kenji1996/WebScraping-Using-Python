import os
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

def iniciarChrome(link):
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument('--log-level=3')
    nav = webdriver.Chrome(options=opcoes)
    nav.get(f"{link}")
    return nav

def acharPar(nav: WebDriver):
    p = nav.find_elements_by_xpath("//div[@id='chapter-content']/p")
    lista_p = []
    for par in p:
        lista_p.append(par.text)
    return lista_p
        

def criarTxt(ln, cap, p: List, dir):
    txt = open(fr"{dir}\{ln}-{cap}"+".txt", "w")
    with txt as file:
        for par in p:
            file.write(par + os.linesep)  
    print("criarTxt done")

def baixarCap(nav: WebDriver, comeco, fim):
    cap = comeco
    for cap in range(fim):
        par = acharPar(nav)
        criarTxt("RMJI", cap+1, par, fr"C:\Programacao\Projetos\Light Novel Extractor Python\teste")
        nav.find_element_by_xpath('//a[@class="btn btn-link"]').click()



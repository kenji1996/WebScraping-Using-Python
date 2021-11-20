from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from func import *

nav = iniciarChrome("https://www.wuxiaworld.com/novel/rmji/rmji-chapter-1")
#string = "https://www.wuxiaworld.com/novel/rmji/rmji-chapter-"
#string = string + "1"
#print(string)

#txt = open(r"C:\Programacao\Projetos\Light Novel Extractor Python\teste\hello.txt", "a")
dir = r"C:\Programacao\Projetos\Light Novel Extractor Python\teste"
baixarCap(nav, 1, 10)
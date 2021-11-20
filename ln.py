import requests, re, copy
from time import gmtime, strftime
from bs4 import BeautifulSoup
import os.path

def getElements(link):
    pag = requests.get(link)
    pag_soup = BeautifulSoup(pag.text, 'html.parser')
    texto = ''
    for elemento in pag_soup.find(id="chapter-content").find_all("p"):
        texto += elemento.text + '\n\n'
    titulo = pag_soup.find('h4', string=re.compile('Chapter')).text + '\n\n'
    hora = strftime("%d-%m-%Y %H:%M:%S", gmtime()) + '\n\n'
    proxPag = "https://www.wuxiaworld.com"+pag_soup.find(class_="next pull-right").find(class_="btn btn-link").get('href')

    return titulo,texto,hora,proxPag

def downloadChapters(dir, nome, inicio, n_cap, link):
    proxpage = link
    for cap in range(inicio, n_cap+1, 1):
        titulo,textos,hora,proxpage = getElements(proxpage)
        file_name = f'{nome} - {cap}'
        dirfile = os.path.join(dir, f'{file_name}.txt')
        f = open(dirfile,"wb+")
        f.write(bytes(titulo+hora+textos, 'utf-8'))
        f.close()
        print(f'Chapter {cap} feito.')
    return print('Todos os capitulos foram baixados.')

downloadChapters(r'D:\Livros\.LIGHTNOVEL\teste', 'RMJI',1,2, 'https://www.wuxiaworld.com/novel/rmji/rmji-chapter-1')


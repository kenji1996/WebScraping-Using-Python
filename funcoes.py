import re
import bs4
import urllib3

def getSoup(url : str):
    http = urllib3.PoolManager()
    resp = http.request(method='GET', url=url)
    data = resp.data
    soup = bs4.BeautifulSoup(data, 'html.parser')
    pret = soup.prettify()
    return pret

def searchElement(frase : str, html_doc : str):
    elemento = re.search(rf'<.*{frase}>', html_doc)
    return elemento
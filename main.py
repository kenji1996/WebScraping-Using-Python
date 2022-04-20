import epub
import webscrapper
import file
import structure
from os import listdir
from os.path import isfile, join

if __name__=="__main__":

    first_page_xhtml = open(r"D:\Livros\.LIGHTNOVEL\Nine Star Hegemon Body Art\0start.xhtml", "w+", encoding='utf-8')
    dir = [fr"D:\Livros\.LIGHTNOVEL\Nine Star Hegemon Body Art\Volume {i}" for i in range(1,11)]
    href = ""

    for i in dir:
        onlyfiles = [f for f in listdir(i) if isfile(join(i, f))]
        for i in onlyfiles:
            href += epub.create_href(i)
            
    toc = epub.create_toc("Nine Star Hegemon Body Art", href)
    first_page_xhtml.write(toc)

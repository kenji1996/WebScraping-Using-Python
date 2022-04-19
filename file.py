import re

def create_file(nome, titulo, textos):

    #tirar caracteres especiais do nome
    nome = re.sub('[^A-Za-z0-9 ]+', '', nome)
    
    f = open(fr'D:\Livros\.LIGHTNOVEL\Nine Star Hegemon Body Art\{nome}.xhtml', 'w', encoding="utf-8")
    p = ""

    for i in textos:
        p += i + '\n'

    estrutura = f"""<?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
    <head>
        <title>{titulo}</title>
    </head>
    <body>
    <h4>{nome}</h4>
    {p}
    </body>
    </html>
    """

    f.write(estrutura)
    f.close()



if __name__=='__main__':

    dir = r"D:\Livros\.LIGHTNOVEL\Nine Star Hegemon Body Art\Volume 10"
    
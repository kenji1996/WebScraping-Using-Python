from os import listdir
from os.path import isfile, join
import re
from PIL import Image, ImageFont, ImageDraw 

# Nine Star Hegemon Body Art - Separated by volumes (WuxiaWorld)
NSHBDA = [(1,119),(119, 235),(235, 312),
          (312, 473),(473, 649),(649, 967),
          (967, 1301),(1301, 1811),(1811, 2357),
          (2357, 2650)]

def is_chapter_missing(dir, volume):

    #getting all files names and sorting if necessary
    onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
    onlyfiles = [i.split() for i in onlyfiles]
    onlyfiles = [int(i[1]) for i in onlyfiles]
    onlyfiles.sort()

    dir_volume = {}

    for i in range(1,11):
        dir_volume[f"Volume {i}"] = [j for j in range(NSHBDA[i-1][0],NSHBDA[i-1][1])]

    for i,j in zip(onlyfiles, dir_volume[f'Volume {volume}']):
        if i != j:
            print(f"capitulo faltando = {j}")
            return j
    return False

def create_href(file):

    #if file is xhtml, otherwise change it
    sub_string = re.sub('.xhtml', '', file)
    titulo = ""

    for i in range(2, len(sub_string)):
        titulo += sub_string[i]

    return f'<p class="calibre_5"><a href="{file}">{titulo}</a></p>\n'

def create_toc(title,href):

    estrutura_toc = f"""        <?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>{title}</title>
        <meta http-equiv="Content-Type" content="text/xhtml; charset=utf-8"/>
        <link rel="stylesheet" type="text/css" href="stylesheet.css"/>
        <link rel="stylesheet" type="text/css" href="page_styles.css"/>
    </head>
    <body class="calibre">
    <p id="filepos8693976" class="calibre_3"><span class="calibre2"><span class="bold">Table of Contents</span></span></p>
    {href}
    <div class="mbp_pagebreak" id="calibre_pb_1403"></div>
    </body>
    </html>"""

    return estrutura_toc
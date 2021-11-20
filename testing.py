from bs4 import BeautifulSoup
import urllib3
import re

from funcoes import getSoup, searchElement

data = getSoup('https://www.wuxiaworld.com/novel/nine-star-hegemon/nshba-chapter-1')

frase = "His mind was a whirl of confusion, and at the same time, severe pain came from all over his body. Long Chen was unable to stop his mind’s chaotic thoughts and emitted a pained groan."

elem = searchElement(frase, data)

print(elem)
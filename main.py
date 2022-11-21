import model.browser_handler as BH
from os import name

if __name__ == "__main__":
    
    handler = BH.BrowserHandler()
    handler.get('https://www.brasildefato.com.br/2022/11/19/bloqueios-golpistas-em-estradas-brasileiras-sao-desarticulados')
    result = handler.search_element('A Polícia Rodoviária Federal (PRF) informou neste sábado (19),')
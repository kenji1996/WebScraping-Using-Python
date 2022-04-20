from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from file import create_file

EMAIL = r"EMAIL"
PW = r"PASSWORD"

def is_empty(valor):
    if valor == "" or valor == None:
        return True
    elif isinstance(valor, list):
        if len(valor) == 0:
            return True
    else:
        return False

def start_chrome():
    LOGGER.setLevel(logging.WARNING)
    options = webdriver.ChromeOptions()

    #pra nao aparecer o browser
    options.add_argument("--headless")

    #oculta os logs que aparece no terminal
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=options)
    
    return browser

def log_in_wuxiaworld(browser):
    url = "https://www.wuxiaworld.com/"
    browser.get(url)
    time.sleep(5)

    #Pagina principal WuxiaWorld
    menu = browser.find_element(By.XPATH, "//button[@aria-label='profile nav']")
    browser.execute_script("arguments[0].click();", menu)
    div_botao_login = browser.find_element(By.XPATH, "//div[@class='MuiGrid-root MuiGrid-container space-x-[10px] ww-tzs92q']")
    botao_login = div_botao_login.find_element(By.XPATH, "//button[@class='border border-blue rounded-[28px] transition-shadow truncate shadow-none font-bold hover:border-blue hover:shadow h-[36px] w-[180px] md:h-[35px] p-0 MuiButton-root m-0 MuiButton-contained text-white whitespace-nowrap bg-[linear-gradient(131.45deg,#20A7FE,#003AFF)] MuiButton-containedPrimary text-[15px] sm:text-[16px] MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButtonBase-root  ww-1lebnu']")
    browser.execute_script("arguments[0].click();", botao_login)

    #Pagina de logar
    time.sleep(2)
    email = browser.find_element_by_id("Username")
    email.send_keys(EMAIL)
    senha = browser.find_element_by_id("Password")
    senha.send_keys(PW)
    botao_logar = browser.find_element(By.XPATH, "//button[@class='w-full rounded-[6px] py-[12px] bg-gradient-to-r from-[#1c9dfe] via-blue to-[#023ff4] text-white text-[15px] font-bold']")
    browser.execute_script("arguments[0].click();", botao_logar)
    time.sleep(2)
    print("Logged")
    browser.refresh()

def get_content(browser):
    first_h4 = browser.find_element_by_tag_name('h4').get_attribute('innerHTML')
    titulo = browser.find_element_by_tag_name('h4').text

    fr_view = browser.find_element(By.CLASS_NAME, 'fr-view')
    p = fr_view.find_elements_by_tag_name('p')
    text = [i.get_attribute('outerHTML') for i in p]
    
    return titulo,first_h4, text

def download_single_chapter(browser, chapter : int):

    url = f"https://www.wuxiaworld.com/novel/nine-star-hegemon/nshba-chapter-{chapter}"
    browser.get(url)
    titulo, nome_capitulo, texto = get_content(browser)
    create_file(titulo, nome_capitulo, texto)
    print(f"Chapter {chapter} downloaded")

def download_multiple_chapters(browser, start, end):
    """ End = capitulo final, NAO ADICIONAR +1 para ajustar range()"""
    i = start

    while i != end+1:

        url = f"https://www.wuxiaworld.com/novel/nine-star-hegemon/nshba-chapter-{i}"
        browser.get(url)
        titulo, nome_capitulo, texto = get_content(browser)
        if is_empty(titulo) or is_empty(nome_capitulo) or is_empty(texto):
            titulo, nome_capitulo, texto = get_content(browser)
        create_file(titulo, nome_capitulo, texto)
        print(f"Chapter {i} now")
        i += 1


if __name__=="__main__":

    browser = start_chrome()
    log_in_wuxiaworld(browser)
    download_multiple_chapters(browser, 2357, 2650)
    browser.close()
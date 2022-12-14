import logging
from lxml import html
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException, NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import re

from src.resources import const, functions
from src.model.elem import Element

class BrowserHandler:

    def __init__(self, browser=None) -> None:

        self.browser = browser
        self.browser = self.create_browser()
        self.html = self.get_current_html()
        self.first_time = True

    def __str__(self) -> str:

        string = f""" \nbrowser: {self.browser}\n
                      current url: {self.browser.current_url}\n"""

        return string

    def get_current_html(self) -> html.HtmlElement:
        # HTML object
        pagina = self.browser.page_source
        pagina = const.PATTERN.sub(lambda m: const.TABLE_REPLACE[re.escape(m.group(0))], pagina)

        # Convert HTML object into string
        root = html.fromstring(pagina)

        return root

    def create_browser(self) -> webdriver.Chrome:
        """ Create Chrome browser.
            Will return 0 if Browser is already instanced at object.browser.

            By default, the browser is headless.

            :param path: If chromedriver.exe is located somewhere else other

            than the project dir."""

        # Check if BrowserHandler.browser is already instanced.
        if isinstance(self.browser, webdriver.chrome.webdriver.WebDriver):
            return 0

        LOGGER.setLevel(logging.WARNING)
        options = webdriver.ChromeOptions()

        # Makes browser invisible
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Hides console log
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        browser = webdriver.Chrome(ChromeDriverManager().install())
        return browser

    def get(self, text: str) -> None:

        """ Access specific website.
        
            Should bypass some safety protocols """

        # webdriver.Chrome only accepts https://something.com, not www.something.com or something.com
        if text[:4] == "www.":
            text = "https://" + text[4:]

        try:
            self.browser.get(text)
            if self.first_time:
                self.first_time = False
                self.html = self.get_current_html()
        except InvalidArgumentException:
            print("Could not enter " + text)

    def search_element(self, text1: str, all=False) -> Element:

        """ Search element that contains certain text. 
            
            :param text1: Text to search 
            :param all: If there's multiple matches, return all. False by Default"""

        try:
            tree = self.html.getroottree()

            # List of elements
            elemento_list = self.html.xpath(f""" //*[contains(text(), '{text1}')] """)
            elem_size = len(elemento_list)

            # Function to build Element object from html.HtmlElement
            def build_elem(elem : html.HtmlElement):
                xpath = tree.getpath(elem)

                elemento = Element()
                elemento.property['class'] = elem.get('class')
                elemento.property['id'] = elem.get('id')
                elemento.property['tag'] = elem.tag
                elemento.property['xpath'] = xpath

                elemento.items = dict( (k, v) for k,v in elem.items()  )
                return elemento

            # If list is empty
            if not elem_size:
                print("Couldn't find any element.")
                return 0

            # List bigger than 1
            elif elem_size > 1:
                """ print("Found more than 1 element with said text") """
                if not all:

                    elemento_list = elemento_list[0]
                    elemento = build_elem(elemento_list)

                    return elemento
                
                elif all:

                    elementos = []
                    for elem in elemento_list:

                        elemento = build_elem(elem)
                        elementos.append(elemento)

                    return elementos

            else:
                elemento_list = elemento_list[0]
                elemento = build_elem(elemento_list)

                return elemento

        # No element contains the text.
        except NoSuchElementException:
            print("Element not found. Maybe try another piece of text.")
            return 0

        # There's a special characters that is not processed correctly.
        except SyntaxError:
            print("The text contains special characters that are not allowed.")
            return 0

        except TimeoutException:
            print("Page took too long to load or element can't be located.")
            return 0

    def find_button_by_url(self, url: str) -> Element:

        result = None

        while result is None:

            try:
                button = self.browser.find_element(
                    By.XPATH, f'//*[@href="{url}"]')
                element = Element()
                element.property = {"id": button.get_attribute('id'),
                                    "class": button.get_attribute('class'),
                                    "tag": button.tag_name}
                result = element
                return result
            except NoSuchElementException:
                print("Couldn't find any button with this link.")
                return 0
    
    def scrape_page(self, el1 : Element, el2 : Element) -> list:

        """ Given 2 different Element objects, search the common xpath
        
            between them and scrape all elements with the same tag"""

        tree = self.html.getroottree()

        el1_tag = el1.property['tag']
        el2_tag = el2.property['tag']

        # Finding similar xpath
        cmm_xpath = functions.get_common_text(elemento1=el1.property['xpath'], elemento2=el2.property['xpath'])
        cmm_div = tree.xpath(cmm_xpath)[0]

        # In case the content have different tags
        if el1_tag == el2_tag:
            content_list = cmm_div.xpath(f'.//{el1_tag}')
        else:
            content_list = cmm_div.xpath(f'.//{el1_tag} | .//{el2_tag}')

        return content_list

    def get_in_between(self, el1 : Element, el2 : Element) -> list:

        """ Given 2 elements in the same div, returns all elements between them. 
            
            Returns a list of all elements found. """

        tree = self.html.getroottree()

        ele1 = tree.xpath(el1.property['xpath'])
        ele1 = ele1[0]

        ele2 = tree.xpath(el2.property['xpath'])
        ele2 = ele2[0]

        el1_div, _ = functions.get_common_text(ele1, ele2)

        tag1 = el1.property['tag']

        el1_div_el = el1_div.xpath(f'./{tag1}')

        start, end = 0,0

        for index, el in enumerate(el1_div_el):
            if el.text_content() == ele1.text_content():
                start = index
            elif el.text_content() == ele2.text_content():
                end = index

        content = [el1_div_el[i].text_content() for i in range(start+1, end)]

        return content

if __name__ == "__main__":
    
    handler = BrowserHandler()
    handler.get('www.python.org')

    about = handler.search_element('About')
    events = handler.search_element('Events')

    a = about.property['xpath']
    e = events.property['xpath']

    xpath = functions.get_common_text(a,e)
import logging
from lxml import html
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException, NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from resources.const import TABLE_REPLACE, PATTERN
import time
import re

class Element:

    def __init__(self) -> None:

        self.property = {
            "id": '',
            "class": '',
            "tag" : '',
            "xpath" : ''
        }


class BrowserHandler:

    def __init__(self, browser=None, path="") -> None:
        """ :param browser: Chrome browser
            :param element: Element object holding info (Default is None) """

        self.browser = browser
        self.path = path
        self.browser = self.create_browser()
        self.first_time = True

    def create_browser(self):
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

        # Hides console log
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        browser = webdriver.Chrome(ChromeDriverManager().install())
        return browser

    def get(self, text: str):

        # webdriver.Chrome only accepts https://something.com, not www.something.com or something.com
        if text[:8] != r'https://':
            text = r'https://' + text

        try:
            self.browser.get(text)
            if self.first_time:
                time.sleep(10)
                self.first_time = False
        except InvalidArgumentException:
            print("Could not enter " + text)

    def search_element(self, text1: str) -> Element():

        """ Search element that contains certain text. 
            
            :param text1: Text to search """

        try:
            # HTML object
            pagina = self.browser.page_source
            pagina = PATTERN.sub(lambda m: TABLE_REPLACE[re.escape(m.group(0))], pagina)

            # Convert HTML object into string
            root = html.fromstring(pagina)
            tree = root.getroottree()

            # List of elements
            elemento_list = root.xpath(f""" //*[contains(text(), '{text1}')] """)
            elem_size = len(elemento_list)

            # If list is empty
            if not elem_size:
                print("Couldn't find any element.")
                return 0

            # List bigger than 1
            elif elem_size > 1:
                print("Found more than 1 element with said text. ONLY the first one will be considered")
                elemento_list = elemento_list[0]

            else:
                elemento_list = elemento_list[0]
                xpath = tree.getpath(elemento_list)

                elemento = Element()
                elemento.property['class'] = elemento_list.get('class')
                elemento.property['id'] = elemento_list.get('id')
                elemento.property['tag'] = elemento_list.tag
                elemento.property['xpath'] = xpath

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

    def find_button(self, url: str):

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
    
    def scrape_page(self, elemento1 : Element, elemento2 : Element):

        pagina = self.browser.page_source
        root = html.fromstring(pagina)
        tree = root.getroottree()


import logging
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException, NoSuchElementException


class Elements:

    def __init__(self) -> None:

        self.url = ''
        self.property = None
        self.div = None


class BrowserHandler:

    def __init__(self, browser=None, path="") -> None:

        """ :param browser: Chrome browser
            :param element: Element object holding info (Default is None) """

        self.browser = browser
        self.path = path
        self.browser = self.create_browser()
        self.element = None

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
        browser = webdriver.Chrome(options=options, executable_path = self.path)
        return browser

    def get(self, text : str):

        #webdriver.Chrome only accepts https://something.com, not www.something.com or something.com
        if text[:8] != r'https://':
            text = r'https://' + text

        try:
            self.browser.get(text)
        except InvalidArgumentException:
            print("Could not enter " + text)

    def search_element_by_text(self, text: str):
        
        """ Search through the browser page for an element that
            contains a piece of text.
            
            :param text: Piece of text."""

        result = None

        while result is None:
            try:
                elemento_temp = self.browser.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
                elemento = Elements()
                elemento.url = self.browser.current_url

                # Store said element's properties for later
                elemento.property = {'id': str(elemento_temp.get_attribute('id')),
                                'class': str(elemento_temp.get_attribute('class')),
                                'tag': str(elemento_temp.tag_name)}

                #Find the parent of elemento_temp (should be a div).
                elemento_temp_div = elemento_temp.find_element(By.XPATH, '..')

                elemento.div = {'class': str(elemento_temp_div.get_attribute('class')),
                                'id': str(elemento_temp_div.get_attribute('id'))}

                result = elemento

            # No element contains the text.    
            except NoSuchElementException:
                print("Element not found. Maybe try another piece of text.")

            # There's a special characters that is not processed correctly.
            except SyntaxError:
                print("The text contains special characters that are not allowed.")

        return result

    def find_button(self, url : str):

        result = None

        while result is None:

            try:
                button = self.browser.find_element(By.XPATH, f'//a[@href="{url}"]')
                element = Elements()
                element.property = {"id": button.get_attribute('id'),
                                    "class": button.get_attribute('class'),
                                    "tag": button.tag_name}
                result = element
                return result
            except NoSuchElementException:
                print("Couldn't find any button with this link.")

    def scrape_page(self):

        if self.element == None:
            print("No sample of page found. Please type a phrase that is part of what should be scrapped.")
            text = input()
            self.element = self.search_element_by_text(text)

        div = self.browser.find_element(By.ID, self.element.div['id'])
        texts = div.find_elements(By.TAG_NAME, self.element.property['tag'])
        texts = [el.text for el in texts]

        return texts

if __name__ == "__main__":

    handler = BrowserHandler()

import logging
import re
from lxml import html
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException, NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from src.resources import const, functions
from src.model.elem import Element

class BrowserHandler:

    def __init__(self, browser=None) -> None:

        self.browser = browser
        self.browser = self.create_browser()
        self.html = self.get_current_html()
        self.first_time = True

    def __str__(self) -> str:

        string = self.__dict__

        return string

    def __repr__(self) -> str:
        
        string = self.__dict__

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

        # Make chrome invisible (careful when debugging, chrome can still be open even without debugging)
        """ options.add_argument("--headless") """

        # Arguments that remove "I'm a bot" flag
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Remove "ERROR:gpu_init.cc(426) Passthrough is not supported, GL is disabled" error
        options.add_argument("--disable-gpu")

        # Hides console log
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        # Change the property value of the navigator for webdriver to undefined
        browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

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
                elemento.property['parent_tag'] = elem.getparent().tag
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
        cmm_xpath, depth = functions.get_common_xpath(el1, el2)
        cmm_div = tree.xpath(cmm_xpath)[0]

        all_el = []

        if max(depth) > 1:

            el1_ptag = el1.property['parent_tag']
            el2_ptag = el2.property['parent_tag']

            cmm_div_allel = cmm_div.xpath(f'./{el1_ptag} | ./{el2_ptag}')

            for el in cmm_div_allel:
                elements = el.xpath(f'./{el1_tag} | ./{el2_tag}')
                for el in elements:
                    all_el.append(el)

        elif max(depth) == 1:

            cmm_div_allel = cmm_div.xpath(f'./{el1_tag} | ./{el2_tag}')

            for el in cmm_div_allel:
                all_el.append(el)

        return all_el

    def get_in_between(self, el1 : Element, el2 : Element, return_elements = False) -> list:

        """ Given 2 elements in the same div, returns all elements between them. 
            
            Returns a list of all elements found. """

        # Local func to handle text comparison/indexation
        def iterate_through(*args : list[html.HtmlElement]):
            
            for arg in args:
                proceed = all(map(lambda x: isinstance(x, html.HtmlElement), arg))
                if not proceed:
                    return print('Not all elements are html.Elements')
                    
            start, end = 0,0

            content_all = []

            for iterable in args:

                for index, el in enumerate(iterable):
                    if el.text_content() == ele1.text_content():
                        start = index
                    elif el.text_content() == ele2.text_content():
                        end = index
                
                # In case you want the elements itself, not the text content only
                if not return_elements:
                    content = [iterable[i].text_content() for i in range(start+1, end)]
                else:
                    content = [iterable[i] for i in range(start+1, end)]

                content_all.append(content)
                del(content)

            return content_all


        tree = self.html.getroottree()

        ele1 = tree.xpath(el1.property['xpath'])
        ele1 = ele1[0]

        ele2 = tree.xpath(el2.property['xpath'])
        ele2 = ele2[0]

        el1_parent_tag = el1.property['parent_tag']
        el2_parent_tag = el2.property['parent_tag']

        div, depths = functions.get_common_xpath(el1, el2)

        el1_div = tree.xpath(div)[0]

        tag1 = el1.property['tag']
        tag2 = el2.property['tag']

        if max(depths) == 1:
            el1_div_el = el1_div.xpath(f'./{tag1}')
            return el1_div_el

        elif max(depths) > 1:

            if el1_parent_tag == el2_parent_tag:

                el1_div_allel = el1_div.xpath(f'./{el1_parent_tag}')
                el1_div_el_per_el = []

                for el in el1_div_allel:

                    elem = el.xpath(f'./{tag1}')
                    if len(elem) == 1:
                        elem = elem[0]
                        el1_div_el_per_el.append(elem)
                    elif len(elem) > 1:
                        for i in elem:
                            el1_div_el_per_el.append(i)

                return iterate_through(el1_div_el_per_el)

            else:

                el1_div_allel = el1_div.xpath(f'./{el1_parent_tag}')
                el2_div_allel = el1_div.xpath(f'./{el2_parent_tag}')

                el_div_el_per_el = []

                for el in el1_div_allel:
                    elem = el.xpath(f'./{tag1}')
                    if len(elem) == 1:
                        elem = elem[0]
                        el_div_el_per_el.append(elem)
                    elif len(elem) > 1:
                        for i in elem:
                            el_div_el_per_el.append(i)

                for el in el2_div_allel:
                    elem = el.xpath(f'./{tag2}')
                    if len(elem) == 1:
                        elem = elem[0]
                        el_div_el_per_el.append(elem)
                    elif len(elem) > 1:
                        for i in elem:
                            el_div_el_per_el.append(i)

                return iterate_through(el_div_el_per_el)

if __name__ == "__main__":
    
    handler = BrowserHandler()
    handler.get('www.python.org')

    about = handler.search_element('About')
    events = handler.search_element('Events')

    content = handler.get_in_between(about, events)
    
    all_content = handler.scrape_page(about, events)
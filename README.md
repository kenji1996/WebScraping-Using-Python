# WebScrapping-Using-Python

`
In this library, you will find functions that will help you extract the desired content from websites using Selenium. You will be able to scrape content from the page by giving a few text samples as base.
`

## Requirements

- `lxml`
- `selenium`
- `webdriver-manager`

## How to use:

First create an instance of `BrowserHandler`:

>   

    # No need to specify chromedriver.exe path
    >>> handler = BrowserHandler()

Enter into the desired page:

>

    >>> handler.get("www.youtube.com")

<br>
<hr/>
<br>
Search desired element:

>


    >>> element = handler.search_element("Home")
    >>> element
    <src.model.browser_handler.Element object at 0x000001686AF13EB0>

    # [ There are 2 attributes of Element, property and items ]
    # Element.property search for specific attributes from the element and holds it.
    # Element.items holds all attributes there is

    >>> element.property
    {'id': None, 'class': None, 'tag': 'script', 'xpath': '/html/head/script[13]', 'text': ''}

    >>> element.items
    {'nonce': 'izOFwYwHVzP4Jiq7oiQHHg'}

`search_element()` can also grab more than 1 element if `PARAMETER all` is `True` (`False` by default)

>

    >>> handler.get('www.python.org')

    >>> handler.search_element('Events', all=True)

    [<__main__.Element object at 0x00000261C5070F70>, <__main__.Element object at 0x00000261C5070F10>, <__main__.Element object at 0x00000261C5070280>, <__main__.Element object at 0x00000261C50702B0>, <__main__.Element object at 0x00000261C5070880>, <__main__.Element object at 0x00000261C50708E0>, <__main__.Element object at 0x00000261C5070850>, <__main__.Element object at 0x00000261C5070A90>, <__main__.Element object at 0x00000261C5077040>, <__main__.Element object at 0x00000261C50770A0>, <__main__.Element object at 0x00000261C5077100>]
    



<br>
<hr/>
<br>

Catch all elements between 2 given elements with `BrowserHandler.get_in_between()`:

>

    >>> handler.get('www.python.org')

    >>> handler

    browser: <selenium.webdriver.chrome.webdriver.WebDriver (session="03786af2dc6f5aba4015dc696c6c105a")>
    current url: https://www.python.org/


![Screenshot](/src/resources/images/pythonorgsite.png)

>

    If I want all elements that's between 'About' and 'Events'...


![Screenshot](/src/resources/images/pythonorgel.png)

>

    >>> about = handler.search_element('About')

    >>> events = handler.search_element('Events')

    >>> handler.get_in_between(about, events)

    [['Downloads', 'Documentation', 'Community', 'Success Stories', 'News']]

We can also use `PARAMETER return_elements` as `TRUE` to get as `html.HtmlElement object` instead

>

    >>> handler.get_in_between(about, events, return_elements=True)

    [[<Element a at 0x1be2606e6d0>, <Element a at 0x1be2606e310>, <Element a at 0x1be2606e720>, <Element a at 0x1be2606e3b0>, <Element a at 0x1be2606e360>]]

<br>
<hr/>
<br>

`BrowserHandler.scrape_page(Element, Element):`

>

    >>> about = handler.search_element('About')

    >>> events = handler.search_element('Events')

    >>> handler.scrape_page(about, events)

    [<Element a at 0x1dd3cca0360>, <Element a at 0x1dd3cca04f0>, <Element a at 0x1dd3cca0590>, <Element a at 0x1dd3cca05e0>, <Element a at 0x1dd3cca0630>, <Element a at 0x1dd3cca0680>, <Element a at 0x1dd3cca0310>]
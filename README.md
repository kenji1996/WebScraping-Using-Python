# WebScrapping-Using-Python

`
In this library, you will find functions that will help you extract the desired content from websites using Selenium. You will be able to scrape content from the page by giving a few text samples as base.
`

## Requirements

- `lxml`
- `selenium`
- `webdriver-manager`

## How to use:

First create an instance of `BrowserHandler`

>   

    # No need to specify chromedriver.exe path
    >>> handler = BrowserHandler()

Enter into the desired page

>

    >>> handler.get("www.youtube.com")

Search desired element

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
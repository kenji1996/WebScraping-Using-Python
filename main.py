import model.browser_handler as BrowserHandler

if __name__ == "__main__":
    
    handler = BrowserHandler()
    handler.get('https://www.wuxiaworld.com/novel/nine-star-hegemon/nshba-chapter-0-1')
    handler.property = handler.search_element_by_text('A small river flowed within the surrounding mountains. Farmland lined the river, and with the sun’s warm rays already lighting up the land, the farmers had long since gotten to work.')
    handler.button = handler.find_button('https://www.wuxiaworld.com/novel/nine-star-hegemon/nshba-chapter-0-2')
    pass

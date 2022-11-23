import model.browser_handler as BH

if __name__ == "__main__":
    
    handler = BH.BrowserHandler()
    handler.get('https://novelbin.net/n/the-desolate-era-novel/chapter-30')
    el1 = handler.search_element('The Aquatic Rhino King, seated on his stone chair, glanced at the bald armored guard.')
    el2 = handler.search_element('Uncle Dala gritted his teeth, then led his tribesmen to flee. As for those of other tribes, they had fled long ago. They had been utterly frightened.')
class Element:

    def __init__(self) -> None:

        self.property = {
            "id": '',
            "class": '',
            "tag" : '',
            "xpath" : '',
            "text": ''
        }

        self.items = {}

    def __str__(self):

        string = "{\n property\n\n"

        for key, item in self.property.items():
            string += f""" {key:<10} : {item:<40}\n"""

        string += "}\n\n{\nitems:\n\n"

        for key, item in self.items.items():
            string += f""" {key:<10} : {item:<40}\n"""

        string += "}"
        
        return string

    def __repr__(self) -> str:
        
        string = "{\n property\n\n"

        for key, item in self.property.items():
            string += f""" {key:<10} : {item:<40}\n"""

        string += "}\n\n{\nitems:\n\n"

        for key, item in self.items.items():
            string += f""" {key:<10} : {item:<40}\n"""

        string += "}"
        
        return string

    
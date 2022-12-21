class Element:

    def __init__(self) -> None:

        self.property = {
            "id": '',
            "class": '',
            "tag" : '',
            "parent_tag": '',
            "xpath" : '',
            "text": ''
        }

        self.items = {}

    def __str__(self):

        return self.__dict__

    def __repr__(self) -> str:
        
        string = "{\n property\n\n"

        for key, item in self.property.items():
            if item is None:
                item = "Empty"
            elif item == "":
                item = "Empty"
            string += f""" {key:<10} : {item:<40}\n"""

        string += "}\n\n{\nitems:\n\n"

        for key, item in self.items.items():
            if item is None:
                item = "Empty"
            elif item == "":
                item = "Empty"
            string += f""" {key:<10} : {item:<40}\n"""

        string += "}"
        
        return string
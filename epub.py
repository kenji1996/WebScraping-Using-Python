class Epub:

    def __init__(self, title, href) -> None:

        """ Epub objects contains title, href and table of content [toc].
        
            TOC is table of references in case there's a term that needs explanation"""

        self.title = title
        self.href = href
        self.table_of_content = self.create_toc(self.title, self.href)

    def create_toc(title,href) -> str:

        estrutura_toc = f"""        <?xml version="1.0" encoding="utf-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"

        "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title>{title}</title>
            <meta http-equiv="Content-Type" content="text/xhtml; charset=utf-8"/>
            <link rel="stylesheet" type="text/css" href="stylesheet.css"/>
            <link rel="stylesheet" type="text/css" href="page_styles.css"/>
        </head>
        <body class="calibre">
        <p id="filepos8693976" class="calibre_3"><span class="calibre2"><span class="bold">Table of Contents</span></span></p>
        {href}
        <div class="mbp_pagebreak" id="calibre_pb_1403"></div>
        </body>
        </html>"""

        return estrutura_toc

    def create_page(self, title, content):

        """ Generates a epub-structure page given a title and content """
        
        # Converting list to string with \n for each element.
        if isinstance(content, list):
            content = '\n'.join(str(e) for e in content)

        page = f"""<?xml version="1.0" encoding="utf-8"?>
        <!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
        <head>
            <title>{title}</title>
        </head>
        <body>
                {content}
        </body>
        </html>
        """
        return page
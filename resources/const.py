import re

# In case the HTML page source comes with "broken" characters that'd make scrapping very hard.
TABLE_REPLACE = {
    r"&nbsp;":" ",
    r"&NewLine;":"\n",
    r"&Tab;":"\t",
    r"&quot;":'\"',
    r"&amp;":r"&"
}

# Redo the dict to fix characters
TABLE_REPLACE = dict((re.escape(k), v) for k, v in TABLE_REPLACE.items())


PATTERN = re.compile("|".join(TABLE_REPLACE.keys()))
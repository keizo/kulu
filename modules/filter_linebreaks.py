"""Replaces line breaks in plain text with appropriate HTML; 
a single newline becomes an HTML line break (<br />) and a 
new line followed by a blank line becomes a paragraph break (</p>).

Borrowed from Django .96
"""

import re

def drupy_filter(text):
    "Converts newlines into <p> and <br />s"
    text = re.sub(r'\r\n|\r|\n', '\n', text) # normalize newlines
    paras = re.split('\n{2,}', text)
    paras = ['<p>%s</p>' % p.strip().replace('\n', '<br />') for p in paras]
    return '\n\n'.join(paras)
"""A filter module for markdown.

Converts text to HTML following the rules of Markdown.
(requires [markdown.py](http://webpy.org/markdown.py))
"""



def drupy_filter(text):
    """Your text can formated using \
    <a href="http://daringfireball.net/projects/markdown/syntax">\
    markdown syntax</a>.
    """
    from markdown import markdown
    if text:
        return markdown(text)
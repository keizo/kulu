"""
Requires sanitize.py
http://www.aaronsw.com/2002/sanitize/sanitize.py
"""
from sanitize import _HTMLSanitizer

class HTMLSanitizer(_HTMLSanitizer):
    acceptable_elements = ['a', 'pre']
    
    acceptable_attributes = ['abbr', 'accept', 'accept-charset', 'accesskey',
      'action', 'align', 'alt', 'axis', 'border', 'cellpadding', 'cellspacing',
      'char', 'charoff', 'charset', 'checked', 'cite', 'class', 'clear', 'cols',
      'colspan', 'color', 'compact', 'coords', 'datetime', 'dir', 'disabled',
      'enctype', 'for', 'frame', 'headers', 'height', 'href', 'hreflang', 'hspace',
      'id', 'ismap', 'label', 'lang', 'longdesc', 'maxlength', 'media', 'method',
      'multiple', 'name', 'nohref', 'noshade', 'nowrap', 'prompt', 'readonly',
      'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope', 'selected', 'shape', 'size',
      'span', 'src', 'start', 'summary', 'tabindex', 'target', 'title', 'type',
      'usemap', 'valign', 'value', 'vspace', 'width']

def drupy_filter(text, encoding='utf8', baseuri=None):
    """Some HTML is allowed."""
    p = HTMLSanitizer(baseuri, encoding)
    p.feed(text)
    data = p.output()
    return data
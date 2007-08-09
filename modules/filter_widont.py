"""
Prevents hanging or widowed words in titles and paragraphs.
Read more at http://shauninman.com/archive/2006/08/22/widont_wordpress_plugin

Borrowed from: http://code.google.com/p/typogrify/

Replaces the space between the last two words in a string with ``&nbsp;``
Works in these block tags ``(h1-h6, p, li)`` and also accounts for 
potential closing inline elements ``a, em, strong, span, b, i``

>>> widont('A very simple test')
'A very simple&nbsp;test'

>>> widont('<p>In a couple of paragraphs</p><p>paragraph two</p>')
'<p>In a couple of&nbsp;paragraphs</p><p>paragraph&nbsp;two</p>'

>>> widont('<h1><a href="#">In a link inside a heading</i> </a></h1>')
'<h1><a href="#">In a link inside a&nbsp;heading</i> </a></h1>'

>>> widont('<h1><a href="#">In a link</a> followed by other text</h1>')
'<h1><a href="#">In a link</a> followed by other&nbsp;text</h1>'

Empty HTMLs shouldn't error
>>> widont('<h1><a href="#"></a></h1>') 
'<h1><a href="#"></a></h1>'

>>> widont('<div>Divs get no love!</div>')
'<div>Divs get no love!</div>'

>>> widont('<div><p>But divs with paragraphs do!</p></div>')
'<div><p>But divs with paragraphs&nbsp;do!</p></div>'
"""

def drupy_filter(text):
    widont_finder = re.compile(r"""(\s+)                                # the space to replace
                                   ([^<>\s]+                            # must be flollowed by non-tag non-space characters
                                   \s*                                  # optional white space! 
                                   (</(a|em|span|strong|i|b)[^>]*>\s*)* # optional closing inline tags with optional white space after each
                                   (</(p|h[1-6]|li)|$))                 # end with a closing p, h1-6, li or the end of the string
                                   """, re.VERBOSE)
    return widont_finder.sub(r'&nbsp;\2', text)

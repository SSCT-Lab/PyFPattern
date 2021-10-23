def html_ify(text):
    ' convert symbols like I(this is in italics) to valid HTML '
    if (not isinstance(text, string_types)):
        text = to_text(text)
    t = html_escape(text)
    t = _ITALIC.sub('<em>\\1</em>', t)
    t = _BOLD.sub('<b>\\1</b>', t)
    t = _MODULE.sub("<span class='module'>\\1</span>", t)
    t = _URL.sub("<a href='\\1'>\\1</a>", t)
    t = _CONST.sub('<code>\\1</code>', t)
    return t
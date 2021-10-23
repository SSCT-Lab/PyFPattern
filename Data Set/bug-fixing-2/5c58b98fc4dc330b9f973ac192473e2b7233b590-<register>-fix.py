

@staticmethod
def register(name, fn_regular, fn_italic=None, fn_bold=None, fn_bolditalic=None):
    "Register an alias for a Font.\n\n        .. versionadded:: 1.1.0\n\n        If you're using a ttf directly, you might not be able to use the\n        bold/italic properties of\n        the ttf version. If the font is delivered in multiple files\n        (one regular, one italic and one bold), then you need to register these\n        files and use the alias instead.\n\n        All the fn_regular/fn_italic/fn_bold parameters are resolved with\n        :func:`kivy.resources.resource_find`. If fn_italic/fn_bold are None,\n        fn_regular will be used instead.\n        "
    fonts = []
    for font_type in (fn_regular, fn_italic, fn_bold, fn_bolditalic):
        if (font_type is not None):
            font = resource_find(font_type)
            if (font is None):
                raise IOError('File {0}s not found'.format(font_type))
            else:
                fonts.append(font)
        else:
            fonts.append(fonts[0])
    LabelBase._fonts[name] = tuple(fonts)

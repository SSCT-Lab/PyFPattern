def load(self, filename):
    if (not filename):
        import traceback
        traceback.print_stack()
        return
    try:
        im = None
        if self._inline:
            im = pygame.image.load(filename, 'x.{}'.format(self._ext))
        elif isfile(filename):
            with open(filename, 'rb') as fd:
                im = pygame.image.load(fd)
        elif isinstance(filename, bytes):
            try:
                fname = filename.decode()
                if isfile(fname):
                    with open(fname, 'rb') as fd:
                        im = pygame.image.load(fd)
            except UnicodeDecodeError:
                pass
        if (im is None):
            im = pygame.image.load(filename)
    except:
        raise
    fmt = ''
    if ((im.get_bytesize() == 3) and (not im.get_colorkey())):
        fmt = 'rgb'
    elif (im.get_bytesize() == 4):
        fmt = 'rgba'
    if (fmt not in ('rgb', 'rgba')):
        try:
            imc = im.convert(32)
            fmt = 'rgba'
        except:
            try:
                imc = im.convert_alpha()
                fmt = 'rgba'
            except:
                Logger.warning(('Image: Unable to convert image %r to rgba (was %r)' % (filename, im.fmt)))
                raise
        im = imc
    if (not self._inline):
        self.filename = filename
    data = pygame.image.tostring(im, fmt.upper())
    return [ImageData(im.get_width(), im.get_height(), fmt, data, source=filename)]
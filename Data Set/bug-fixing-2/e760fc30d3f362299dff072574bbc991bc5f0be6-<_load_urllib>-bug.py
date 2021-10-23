

def _load_urllib(self, filename, kwargs):
    '(internal) Loading a network file. First download it, save it to a\n        temporary file, and pass it to _load_local().'
    if PY2:
        import urllib2 as urllib_request

        def gettype(info):
            return info.gettype()
    else:
        import urllib.request as urllib_request

        def gettype(info):
            return info.get_content_type()
    proto = filename.split(':', 1)[0]
    if (proto == 'smb'):
        try:
            from smb.SMBHandler import SMBHandler
        except ImportError:
            Logger.warning('Loader: can not load PySMB: make sure it is installed')
            return
    import tempfile
    data = fd = _out_osfd = None
    try:
        _out_filename = ''
        if (proto == 'smb'):
            fd = urllib_request.build_opener(SMBHandler).open(filename)
        else:
            fd = urllib_request.urlopen(filename)
        if ('#.' in filename):
            suffix = ('.' + filename.split('#.')[(- 1)])
        else:
            ctype = gettype(fd.info())
            suffix = mimetypes.guess_extension(ctype)
            if (not suffix):
                parts = filename.split('?')[0].split('/')[1:]
                while ((len(parts) > 1) and (not parts[0])):
                    parts = parts[1:]
                if ((len(parts) > 1) and ('.' in parts[(- 1)])):
                    suffix = ('.' + parts[(- 1)].split('.')[(- 1)])
        (_out_osfd, _out_filename) = tempfile.mkstemp(prefix='kivyloader', suffix=suffix)
        idata = fd.read()
        fd.close()
        fd = None
        write(_out_osfd, idata)
        close(_out_osfd)
        _out_osfd = None
        data = self._load_local(_out_filename, kwargs)
        for imdata in data._data:
            imdata.source = filename
    except Exception:
        Logger.exception(('Loader: Failed to load image <%s>' % filename))
        try:
            close(_out_osfd)
        except OSError:
            pass
        return self.error_image
    finally:
        if fd:
            fd.close()
        if _out_osfd:
            close(_out_osfd)
        if (_out_filename != ''):
            unlink(_out_filename)
    return data

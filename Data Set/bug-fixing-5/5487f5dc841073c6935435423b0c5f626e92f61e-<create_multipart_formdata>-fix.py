def create_multipart_formdata(files, fields=None, send_8kb=False):
    'Create the data for a multipart/form request.\n\n    :param list(list) files: list of lists each containing (name, filename, path).\n    :param list(list) fields: list of lists each containing (key, value).\n    :param bool send_8kb: only sends the first 8kb of the files (default: False).\n    '
    boundary = ('---------------------------' + ''.join([str(random.randint(0, 9)) for x in range(27)]))
    data_parts = list()
    data = None
    if six.PY2:
        newline = '\r\n'
        if (fields is not None):
            for (key, value) in fields:
                data_parts.extend([('--%s' % boundary), ('Content-Disposition: form-data; name="%s"' % key), '', value])
        for (name, filename, path) in files:
            with open(path, 'rb') as fh:
                value = (fh.read(8192) if send_8kb else fh.read())
                data_parts.extend([('--%s' % boundary), ('Content-Disposition: form-data; name="%s"; filename="%s"' % (name, filename)), ('Content-Type: %s' % (mimetypes.guess_type(path)[0] or 'application/octet-stream')), '', value])
        data_parts.extend([('--%s--' % boundary), ''])
        data = newline.join(data_parts)
    else:
        newline = six.b('\r\n')
        if (fields is not None):
            for (key, value) in fields:
                data_parts.extend([six.b(('--%s' % boundary)), six.b(('Content-Disposition: form-data; name="%s"' % key)), six.b(''), six.b(value)])
        for (name, filename, path) in files:
            with open(path, 'rb') as fh:
                value = (fh.read(8192) if send_8kb else fh.read())
                data_parts.extend([six.b(('--%s' % boundary)), six.b(('Content-Disposition: form-data; name="%s"; filename="%s"' % (name, filename))), six.b(('Content-Type: %s' % (mimetypes.guess_type(path)[0] or 'application/octet-stream'))), six.b(''), value])
        data_parts.extend([six.b(('--%s--' % boundary)), b''])
        data = newline.join(data_parts)
    headers = {
        'Content-Type': ('multipart/form-data; boundary=%s' % boundary),
        'Content-Length': str(len(data)),
    }
    return (headers, data)
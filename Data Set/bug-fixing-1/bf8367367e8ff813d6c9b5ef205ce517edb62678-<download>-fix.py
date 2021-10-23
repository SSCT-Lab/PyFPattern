

def download(url, module_name, md5sum, save_name=None):
    dirname = os.path.join(DATA_HOME, module_name)
    if (not os.path.exists(dirname)):
        os.makedirs(dirname)
    filename = os.path.join(dirname, (url.split('/')[(- 1)] if (save_name is None) else save_name))
    if (os.path.exists(filename) and (md5file(filename) == md5sum)):
        return filename
    retry = 0
    retry_limit = 3
    while (not (os.path.exists(filename) and (md5file(filename) == md5sum))):
        if os.path.exists(filename):
            sys.stderr.write(('file %s  md5 %s' % (md5file(filename), md5sum)))
        if (retry < retry_limit):
            retry += 1
        else:
            raise RuntimeError('Cannot download {0} within retry limit {1}'.format(url, retry_limit))
        sys.stderr.write(('Cache file %s not found, downloading %s' % (filename, url)))
        r = requests.get(url, stream=True)
        total_length = r.headers.get('content-length')
        if (total_length is None):
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            with open(filename, 'wb') as f:
                dl = 0
                total_length = int(total_length)
                for data in r.iter_content(chunk_size=4096):
                    if six.PY2:
                        data = six.b(data)
                    dl += len(data)
                    f.write(data)
                    done = int(((50 * dl) / total_length))
                    sys.stderr.write(('\r[%s%s]' % (('=' * done), (' ' * (50 - done)))))
                    sys.stdout.flush()
    sys.stderr.write('\n')
    sys.stdout.flush()
    return filename

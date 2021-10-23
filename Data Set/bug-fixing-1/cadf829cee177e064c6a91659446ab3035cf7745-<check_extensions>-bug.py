

def check_extensions(extensions):
    for x in extensions:
        for f in x.sources:
            if (not path.isfile(f)):
                msg = ((('Missing file: %s\n' % f) + 'Please install Cython.\n') + 'See http://docs.chainer.org/en/stable/install.html')
                raise RuntimeError(msg)

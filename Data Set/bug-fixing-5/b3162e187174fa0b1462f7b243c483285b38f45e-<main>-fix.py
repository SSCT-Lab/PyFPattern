def main():
    p = optparse.OptionParser(__doc__)
    (options, args) = p.parse_args()
    if (len(args) < 1):
        p.error('no mode given')
    mode = args.pop(0)
    if (mode not in ('html', 'tex')):
        p.error(('unknown mode %s' % mode))

    def _open(fn, *args, **kwargs):
        'Handle UTF-8 encoding when loading under Py3'
        if (sys.version_info.major < 3):
            return open(fn, *args, **kwargs)
        return io.open(fn, *args, encoding='utf-8', **kwargs)
    for fn in args:
        with _open(fn, 'r') as f:
            if (mode == 'html'):
                lines = process_html(fn, f.readlines())
            elif (mode == 'tex'):
                lines = process_tex(f.readlines())
        with _open(fn, 'w') as f:
            f.write(''.join(lines))
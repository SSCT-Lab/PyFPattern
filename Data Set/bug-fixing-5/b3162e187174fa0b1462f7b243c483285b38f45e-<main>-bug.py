def main():
    p = optparse.OptionParser(__doc__)
    (options, args) = p.parse_args()
    if (len(args) < 1):
        p.error('no mode given')
    mode = args.pop(0)
    if (mode not in ('html', 'tex')):
        p.error(('unknown mode %s' % mode))
    for fn in args:
        f = open(fn, 'r')
        try:
            if (mode == 'html'):
                lines = process_html(fn, f.readlines())
            elif (mode == 'tex'):
                lines = process_tex(f.readlines())
        finally:
            f.close()
        f = open(fn, 'w')
        f.write(''.join(lines))
        f.close()
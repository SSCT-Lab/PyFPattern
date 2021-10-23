

def fetch(version):
    base = 'http://wheels.scipy.org'
    tree = html.parse(base)
    root = tree.getroot()
    dest = pathlib.Path('dist')
    dest.mkdir(exist_ok=True)
    files = [x for x in root.xpath('//a/text()') if (x.startswith('pandas-{}'.format(version)) and (not dest.joinpath(x).exists()))]
    N = len(files)
    for (i, filename) in enumerate(files, 1):
        out = str(dest.joinpath(filename))
        link = urllib.request.urljoin(base, filename)
        urllib.request.urlretrieve(link, out)
        print('Downloaded {link} to {out} [{i}/{N}]'.format(link=link, out=out, i=i, N=N))

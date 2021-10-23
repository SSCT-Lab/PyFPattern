def extract(fpath, exdir):
    print('Extracting zip file')
    with ZipFile(fpath) as z:
        z.extractall(path=exdir)
    print('Extracting Done')
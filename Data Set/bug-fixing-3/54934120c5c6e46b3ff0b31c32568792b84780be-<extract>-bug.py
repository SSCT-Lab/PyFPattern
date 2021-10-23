def extract(fpath):
    print('Extracting zip file')
    with ZipFile(fpath) as z:
        z.extractall(path='./')
    print('Extracting Done')
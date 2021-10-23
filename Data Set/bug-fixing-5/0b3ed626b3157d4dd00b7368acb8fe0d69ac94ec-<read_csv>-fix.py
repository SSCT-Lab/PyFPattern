def read_csv(self, filename, key, delimiter, encoding='utf-8', dflt=None, col=1):
    try:
        f = open(filename, 'rb')
        creader = CSVReader(f, delimiter=to_native(delimiter), encoding=encoding)
        for row in creader:
            if (len(row) and (row[0] == key)):
                return row[int(col)]
    except Exception as e:
        raise AnsibleError(('csvfile: %s' % to_native(e)))
    return dflt
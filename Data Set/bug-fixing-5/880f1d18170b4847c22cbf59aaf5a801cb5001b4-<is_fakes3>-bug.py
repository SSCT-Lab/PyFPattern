def is_fakes3(s3_url):
    ' Return True if s3_url has scheme fakes3:// '
    if (s3_url is not None):
        return (urlparse.urlparse(s3_url).scheme in ('fakes3', 'fakes3s'))
    else:
        return False
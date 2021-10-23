def is_walrus(s3_url):
    " Return True if it's Walrus endpoint, not S3\n\n    We assume anything other than *.amazonaws.com is Walrus"
    if (s3_url is not None):
        o = urlparse(s3_url)
        return (not o.hostname.endswith('amazonaws.com'))
    else:
        return False
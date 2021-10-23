def get_s3_connection(aws_connect_kwargs, location, rgw, s3_url):
    if (s3_url and rgw):
        rgw = urlparse(s3_url)
        for kw in ['is_secure', 'host', 'port', 'calling_format']:
            try:
                del aws_connect_kwargs[kw]
            except KeyError:
                pass
        s3 = boto.connect_s3(is_secure=(rgw.scheme == 'https'), host=rgw.hostname, port=rgw.port, calling_format=OrdinaryCallingFormat(), **aws_connect_kwargs)
    elif is_fakes3(s3_url):
        fakes3 = urlparse(s3_url)
        for kw in ['is_secure', 'host', 'port', 'calling_format']:
            try:
                del aws_connect_kwargs[kw]
            except KeyError:
                pass
        s3 = S3Connection(is_secure=(fakes3.scheme == 'fakes3s'), host=fakes3.hostname, port=fakes3.port, calling_format=OrdinaryCallingFormat(), **aws_connect_kwargs)
    elif is_walrus(s3_url):
        walrus = urlparse(s3_url).hostname
        s3 = boto.connect_walrus(walrus, **aws_connect_kwargs)
    else:
        aws_connect_kwargs['is_secure'] = True
        try:
            s3 = connect_to_aws(boto.s3, location, **aws_connect_kwargs)
        except AnsibleAWSError:
            s3 = boto.connect_s3(**aws_connect_kwargs)
    return s3
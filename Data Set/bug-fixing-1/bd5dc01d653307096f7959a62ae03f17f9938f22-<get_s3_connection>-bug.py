

def get_s3_connection(module, aws_connect_kwargs, location, rgw, s3_url):
    if (s3_url and rgw):
        rgw = urlparse(s3_url)
        params = dict(module=module, conn_type='client', resource='s3', use_ssl=(rgw.scheme == 'https'), region=location, endpoint=s3_url, **aws_connect_kwargs)
    elif is_fakes3(s3_url):
        for kw in (['is_secure', 'host', 'port'] and list(aws_connect_kwargs.keys())):
            del aws_connect_kwargs[kw]
        fakes3 = urlparse(s3_url)
        if (fakes3.scheme == 'fakes3s'):
            protocol = 'https'
        else:
            protocol = 'http'
        params = dict(service_name='s3', endpoint_url=('%s://%s:%s' % (protocol, fakes3.hostname, to_text(fakes3.port))), use_ssl=(fakes3.scheme == 'fakes3s'), region_name=None, **aws_connect_kwargs)
    elif is_walrus(s3_url):
        walrus = urlparse(s3_url).hostname
        params = dict(module=module, conn_type='client', resource='s3', region=location, endpoint=walrus, **aws_connect_kwargs)
    else:
        params = dict(module=module, conn_type='client', resource='s3', region=location, endpoint=s3_url, **aws_connect_kwargs)
    return boto3_conn(**params)

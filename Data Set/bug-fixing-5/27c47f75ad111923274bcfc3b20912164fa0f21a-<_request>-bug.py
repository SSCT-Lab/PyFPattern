def _request(self, url, failmsg, f):
    url_to_use = url
    parsed_url = urlparse(url)
    if (parsed_url.scheme == 's3'):
        parsed_url = urlparse(url)
        bucket_name = parsed_url.netloc
        key_name = parsed_url.path[1:]
        client = boto3.client('s3', aws_access_key_id=self.module.params.get('username', ''), aws_secret_access_key=self.module.params.get('password', ''))
        url_to_use = client.generate_presigned_url('get_object', Params={
            'Bucket': bucket_name,
            'Key': key_name,
        }, ExpiresIn=10)
    req_timeout = self.module.params.get('timeout')
    self.module.params['url_username'] = self.module.params.get('username', '')
    self.module.params['url_password'] = self.module.params.get('password', '')
    self.module.params['http_agent'] = self.module.params.get('user_agent', None)
    (response, info) = fetch_url(self.module, url_to_use, timeout=req_timeout)
    if (info['status'] != 200):
        raise ValueError(((((failmsg + ' because of ') + info['msg']) + 'for URL ') + url_to_use))
    else:
        return f(response)
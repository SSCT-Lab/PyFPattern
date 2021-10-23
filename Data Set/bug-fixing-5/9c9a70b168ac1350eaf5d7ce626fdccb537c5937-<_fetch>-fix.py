def _fetch(self, url):
    (response, info) = fetch_url(self.module, url, force=True)
    if (info.get('status') not in (200, 404)):
        time.sleep(3)
        self.module.warn('Retrying query to metadata service. First attempt failed: {0}'.format(info['msg']))
        (response, info) = fetch_url(self.module, url, force=True)
        if (info.get('status') not in (200, 404)):
            self.module.fail_json(msg='Failed to retrieve metadata from AWS: {0}'.format(info['msg']), response=info)
    if response:
        data = response.read()
    else:
        data = None
    return to_text(data)
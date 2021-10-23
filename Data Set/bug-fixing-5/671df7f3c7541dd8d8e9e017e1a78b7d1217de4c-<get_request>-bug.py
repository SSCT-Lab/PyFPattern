def get_request(self, uri):
    try:
        resp = open_url(uri, method='GET', url_username=self.creds['user'], url_password=self.creds['pswd'], force_basic_auth=True, validate_certs=False, follow_redirects='all', use_proxy=False, timeout=self.timeout)
        data = json.loads(resp.read())
    except HTTPError as e:
        return {
            'ret': False,
            'msg': ('HTTP Error: %s' % e.code),
        }
    except URLError as e:
        return {
            'ret': False,
            'msg': ('URL Error: %s' % e.reason),
        }
    except Exception as e:
        return {
            'ret': False,
            'msg': ('Failed GET operation against Redfish API server: %s' % to_text(e)),
        }
    return {
        'ret': True,
        'data': data,
    }
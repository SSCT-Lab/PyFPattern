def get_request(self, uri):
    try:
        resp = open_url(uri, method='GET', url_username=self.creds['user'], url_password=self.creds['pswd'], force_basic_auth=True, validate_certs=False, timeout=10, use_proxy=False)
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
    except:
        return {
            'ret': False,
            'msg': 'Unknown error',
        }
    return {
        'ret': True,
        'data': data,
    }
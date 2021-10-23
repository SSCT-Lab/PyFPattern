def patch_request(self, uri, pyld, hdrs):
    try:
        resp = open_url(uri, data=json.dumps(pyld), headers=hdrs, method='PATCH', url_username=self.creds['user'], url_password=self.creds['pswd'], force_basic_auth=True, validate_certs=False, follow_redirects='all', use_proxy=False, timeout=self.timeout)
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
            'msg': ('Failed PATCH operation against Redfish API server: %s' % to_text(e)),
        }
    return {
        'ret': True,
        'resp': resp,
    }
def delete_request(self, uri, pyld, hdrs):
    try:
        resp = open_url(uri, data=json.dumps(pyld), headers=hdrs, method='DELETE', url_username=self.creds['user'], url_password=self.creds['pswd'], force_basic_auth=True, validate_certs=False, follow_redirects='all', use_proxy=False, timeout=self.timeout)
    except HTTPError as e:
        msg = self._get_extended_message(e)
        return {
            'ret': False,
            'msg': ("HTTP Error %s on DELETE request to '%s', extended message: '%s'" % (e.code, uri, msg)),
        }
    except URLError as e:
        return {
            'ret': False,
            'msg': ("URL Error on DELETE request to '%s': '%s'" % (uri, e.reason)),
        }
    except Exception as e:
        return {
            'ret': False,
            'msg': ("Failed DELETE request to '%s': '%s'" % (uri, to_text(e))),
        }
    return {
        'ret': True,
        'resp': resp,
    }


def send(self, url, method='GET', data=None):
    url = self._url_builder(url)
    data = json.dumps(data)
    try:
        if (method == 'GET'):
            resp_data = {
                
            }
            incomplete = True
            while incomplete:
                resp = requests.get(url, data=data, headers=self.headers, timeout=self.timeout)
                json_resp = resp.json()
                for (key, value) in json_resp.items():
                    if (isinstance(value, list) and (key in resp_data)):
                        resp_data[key] += value
                    else:
                        resp_data[key] = value
                try:
                    url = json_resp['links']['pages']['next']
                except KeyError:
                    incomplete = False
    except ValueError as e:
        sys.exit(('Unable to parse result from %s: %s' % (url, e)))
    return json_resp

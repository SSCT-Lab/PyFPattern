def update_auth(self, response, response_text):
    '\n        Get cookies and obtain value for csrftoken that will be used on next requests\n        :param response: Response given by the server.\n        :param response_text Unused_input.\n        :return: Dictionary containing headers\n        '
    headers = {
        
    }
    resp_raw_headers = []
    if hasattr(response.headers, '_headers'):
        resp_raw_headers = response.headers._headers
    else:
        resp_raw_headers = [(attr, response.headers[attr]) for attr in response.headers]
    for (attr, val) in resp_raw_headers:
        if ((attr.lower() == 'set-cookie') and ('APSCOOKIE_' in val)):
            headers['Cookie'] = val
            x_ccsrftoken_position = val.find('ccsrftoken=')
            if (x_ccsrftoken_position != (- 1)):
                token_string = val[(x_ccsrftoken_position + len('ccsrftoken=')):].split('"')[1]
                self._ccsrftoken = token_string
        elif ((attr.lower() == 'set-cookie') and ('ccsrftoken=' in val)):
            csrftoken_search = re.search('"(.*)"', val)
            if csrftoken_search:
                self._ccsrftoken = csrftoken_search.group(1)
    headers['x-csrftoken'] = self._ccsrftoken
    return headers
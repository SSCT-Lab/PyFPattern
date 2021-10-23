def update_auth(self, response, response_text):
    '\n        Get cookies and obtain value for csrftoken that will be used on next requests\n        :param response: Response given by the server.\n        :param response_text Unused_input.\n        :return: Dictionary containing headers\n        '
    headers = {
        
    }
    for (attr, val) in response.getheaders():
        if ((attr == 'Set-Cookie') and ('APSCOOKIE_' in val)):
            headers['Cookie'] = val
        elif ((attr == 'Set-Cookie') and ('ccsrftoken=' in val)):
            csrftoken_search = re.search('"(.*)"', val)
            if csrftoken_search:
                self._ccsrftoken = csrftoken_search.group(1)
    headers['x-csrftoken'] = self._ccsrftoken
    return headers
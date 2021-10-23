

def decode_result(self, result, resp):
    'Decode the result fetched from url according to his Content-Type.\n        Currently supports only application/json.\n        '
    content_type = resp.getheader('Content-Type', None)
    if (content_type is not None):
        ct = content_type.split(';')[0]
        if (ct == 'application/json'):
            if isinstance(result, bytes):
                result = result.decode('utf-8')
            try:
                return loads(result)
            except:
                return result
    return result

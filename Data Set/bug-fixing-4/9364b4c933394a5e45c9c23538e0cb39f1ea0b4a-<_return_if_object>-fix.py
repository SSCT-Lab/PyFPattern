def _return_if_object(self, module, response):
    '\n            :param module: A GcpModule\n            :param response: A Requests response object\n            :return JSON response\n        '
    if (response.status_code == 404):
        return None
    if (response.status_code == 204):
        return None
    try:
        response.raise_for_status
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError) as inst:
        module.fail_json(msg=('Invalid JSON response with error: %s' % inst))
    except GcpRequestException as inst:
        module.fail_json(msg=('Network error: %s' % inst))
    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))
    return result
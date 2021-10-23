def _construct_opmessage(self, operation):
    'Construct operation message.\n\n        Args:\n            operation: operation to construct the message\n\n        Returns:\n            dict: constructed operation message\n        '
    try:
        return {
            'default_msg': ('0' if (('message' in operation) or ('subject' in operation)) else '1'),
            'mediatypeid': (self._zapi_wrapper.get_mediatype_by_mediatype_name(operation.get('media_type')) if (operation.get('media_type') is not None) else '0'),
            'message': operation.get('message'),
            'subject': operation.get('subject'),
        }
    except Exception as e:
        self._module.fail_json(msg=('Failed to construct operation message. The error was: %s' % e))
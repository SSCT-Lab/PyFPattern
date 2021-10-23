def get_mediatype_by_mediatype_name(self, mediatype_name):
    'Get mediatype by mediatype name\n\n        Args:\n            mediatype_name: mediatype name\n\n        Returns:\n            mediatype matching mediatype name\n\n        '
    try:
        mediatype_list = self._zapi.mediatype.get({
            'output': 'extend',
            'selectInventory': 'extend',
            'filter': {
                'description': [mediatype_name],
            },
        })
        if (len(mediatype_list) < 1):
            self._module.fail_json(msg=('Media type not found: %s' % mediatype_name))
        else:
            return mediatype_list[0]
    except Exception as e:
        self._module.fail_json(msg=("Failed to get mediatype '%s': %s" % (mediatype_name, e)))
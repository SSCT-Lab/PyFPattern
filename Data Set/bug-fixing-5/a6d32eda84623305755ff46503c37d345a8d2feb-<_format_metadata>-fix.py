def _format_metadata(self, metadata):
    '\n            :param metadata: A list of dicts where each dict has keys "key" and "value"\n            :return a dict with key/value pairs for each in list.\n        '
    new_metadata = {
        
    }
    for pair in metadata:
        new_metadata[pair['key']] = pair['value']
    return new_metadata
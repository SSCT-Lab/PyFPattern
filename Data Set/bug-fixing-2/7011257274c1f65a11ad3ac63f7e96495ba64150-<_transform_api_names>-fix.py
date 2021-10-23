

def _transform_api_names(self, item):
    if (('subPath' in item) and (item['subPath'] is None)):
        return item['name']
    result = transform_name(item['fullPath'])
    return result

def keyed_list_helper(self, list_to_key):
    keyed_list = dict()
    for item in list_to_key:
        distribution_id = item['Id']
        if ('Items' in item['Aliases']):
            aliases = item['Aliases']['Items']
            for alias in aliases:
                keyed_list.update({
                    alias: item,
                })
        keyed_list.update({
            distribution_id: item,
        })
    return keyed_list
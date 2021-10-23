def keyed_list_helper(self, list_to_key):
    keyed_list = dict()
    for item in list_to_key:
        aliases = item['Aliases']['Items']
        distribution_id = item['Id']
        keyed_list.update({
            distribution_id: item,
        })
        for alias in aliases:
            keyed_list.update({
                alias: item,
            })
    return keyed_list
def get_aliases_from_distribution_id(self, distribution_id):
    aliases = []
    try:
        distributions = self.list_distributions(False)
        for dist in distributions:
            if ((dist['Id'] == distribution_id) and ('Items' in dist['Aliases'])):
                for alias in dist['Aliases']['Items']:
                    aliases.append(alias)
                break
        return aliases
    except Exception as e:
        self.module.fail_json(msg=('Error getting list of aliases from distribution_id - ' + str(e)), exception=traceback.format_exc(e))
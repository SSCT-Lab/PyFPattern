def get_distribution_id_from_domain_name(self, domain_name):
    try:
        distribution_id = ''
        distributions = self.list_distributions(False)
        for dist in distributions:
            for alias in dist['Aliases']['Items']:
                if (str(alias).lower() == domain_name.lower()):
                    distribution_id = str(dist['Id'])
                    break
        return distribution_id
    except Exception as e:
        self.module.fail_json(msg=('Error getting distribution id from domain name = ' + str(e)), exception=traceback.format_exc(e))
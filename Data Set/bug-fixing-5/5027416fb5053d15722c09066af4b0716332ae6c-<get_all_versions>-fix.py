def get_all_versions(self, location, version):
    '\n        Get all kubernetes version supported by AKS\n        :return: ordered version list\n        '
    try:
        result = dict()
        response = self.containerservice_client.container_services.list_orchestrators(self.location, resource_type='managedClusters')
        orchestrators = response.orchestrators
        for item in orchestrators:
            result[item.orchestrator_version] = ([x.orchestrator_version for x in item.upgrades] if item.upgrades else [])
        if version:
            return (result.get(version) or [])
        else:
            keys = list(result.keys())
            keys.sort()
            return keys
    except Exception as exc:
        self.fail('Error when getting AKS supported kubernetes version list for location {0} - {1}'.format(self.location, (exc.message or str(exc))))
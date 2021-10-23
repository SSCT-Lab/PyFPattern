def describe_services(self, cluster, services):
    fn_args = dict()
    if (cluster and (cluster is not None)):
        fn_args['cluster'] = cluster
    fn_args['services'] = services.split(',')
    response = self.ecs.describe_services(**fn_args)
    relevant_response = {
        'services': [],
    }
    for service in response.get('services', []):
        relevant_response['services'].append(self.extract_service_from(service))
    if (('failures' in response) and (len(response['failures']) > 0)):
        relevant_response['services_not_running'] = response['failures']
    return relevant_response
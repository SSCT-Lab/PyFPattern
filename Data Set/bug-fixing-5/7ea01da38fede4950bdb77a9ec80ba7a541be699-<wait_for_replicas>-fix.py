def wait_for_replicas(self, replicas):
    ' Wait for ready_replicas to equal the requested number of replicas. '
    resource = self.find_supported_resource(KIND)
    return_obj = None
    for event in resource.watch(namespace=self.namespace, timeout=self.params.get('wait_timeout')):
        entity = event['object']
        if (entity.metadata.name != self.name):
            continue
        status = entity.get('status', {
            
        })
        readyReplicas = status.get('readyReplicas', 0)
        if (readyReplicas == replicas):
            return_obj = entity
            break
    if (not return_obj):
        self.fail_json(msg='Error fetching the patched object. Try a higher wait_timeout value.')
    if (replicas and (return_obj.status.readyReplicas is None)):
        self.fail_json(msg='Failed to fetch the number of ready replicas. Try a higher wait_timeout value.')
    if (replicas and (return_obj.status.readyReplicas != replicas)):
        self.fail_json(msg='Number of ready replicas is {0}. Failed to reach {1} ready replicas within the wait_timeout period.'.format(return_obj.status.ready_replicas, replicas))
    return return_obj.to_dict()
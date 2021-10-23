def wait(self, resource, definition, timeout, state='present'):

    def _deployment_ready(deployment):
        return (deployment.status and (deployment.status.replicas is not None) and (deployment.status.availableReplicas == deployment.status.replicas) and (deployment.status.observedGeneration == deployment.metadata.generation))

    def _pod_ready(pod):
        return (pod.status and (pod.status.containerStatuses is not None) and all([container.ready for container in pod.status.containerStatuses]))

    def _daemonset_ready(daemonset):
        return (daemonset.status and (daemonset.status.desiredNumberScheduled is not None) and (daemonset.status.numberReady == daemonset.status.desiredNumberScheduled) and (daemonset.status.observedGeneration == daemonset.metadata.generation))

    def _resource_absent(resource):
        return (not resource)
    waiter = dict(Deployment=_deployment_ready, DaemonSet=_daemonset_ready, Pod=_pod_ready)
    kind = definition['kind']
    if (state == 'present'):
        predicate = waiter.get(kind, (lambda x: True))
    else:
        predicate = _resource_absent
    return self._wait_for(resource, definition['metadata']['name'], definition['metadata']['namespace'], predicate, timeout, state)
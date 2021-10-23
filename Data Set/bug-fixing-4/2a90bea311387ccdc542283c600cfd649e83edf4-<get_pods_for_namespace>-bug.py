def get_pods_for_namespace(self, client, name, namespace):
    v1_pod = client.resources.get(api_version='v1', kind='Pod')
    try:
        obj = v1_pod.get(namespace=namespace)
    except DynamicApiError as exc:
        raise K8sInventoryException('Error fetching Pod list: {0}'.format(exc.message))
    namespace_group = 'namespace_{0}'.format(namespace)
    namespace_pods_group = '{0}_pods'.format(namespace_group)
    self.inventory.add_group(name)
    self.inventory.add_group(namespace_group)
    self.inventory.add_child(name, namespace_group)
    self.inventory.add_group(namespace_pods_group)
    self.inventory.add_child(namespace_group, namespace_pods_group)
    for pod in obj.items:
        pod_name = pod.metadata.name
        pod_groups = []
        pod_labels = ({
            
        } if (not pod.metadata.labels) else pod.metadata.labels)
        pod_annotations = ({
            
        } if (not pod.metadata.annotations) else pod.metadata.annotations)
        if pod.metadata.labels:
            pod_labels = pod.metadata.labels
            for (key, value) in pod.metadata.labels:
                group_name = 'label_{0}_{1}'.format(key, value)
                if (group_name not in pod_groups):
                    pod_groups.append(group_name)
                self.inventory.add_group(group_name)
        for container in pod.status.containerStatuses:
            container_name = '{0}_{1}'.format(pod.metadata.name, container.name)
            self.inventory.add_host(container_name)
            self.inventory.add_child(namespace_pods_group, container_name)
            if pod_groups:
                for group in pod_groups:
                    self.inventory.add_child(group, container_name)
            self.inventory.set_variable(container_name, 'object_type', 'pod')
            self.inventory.set_variable(container_name, 'labels', pod_labels)
            self.inventory.set_variable(container_name, 'annotations', pod_annotations)
            self.inventory.set_variable(container_name, 'cluster_name', pod.metadata.clusterName)
            self.inventory.set_variable(container_name, 'pod_node_name', pod.spec.nodeName)
            self.inventory.set_variable(container_name, 'pod_name', pod.spec.name)
            self.inventory.set_variable(container_name, 'pod_host_ip', pod.status.hostIP)
            self.inventory.set_variable(container_name, 'pod_phase', pod.status.phase)
            self.inventory.set_variable(container_name, 'pod_ip', pod.status.podIP)
            self.inventory.set_variable(container_name, 'pod_self_link', pod.metadata.selfLink)
            self.inventory.set_variable(container_name, 'pod_resource_version', pod.metadata.resourceVersion)
            self.inventory.set_variable(container_name, 'pod_uid', pod.metadata.uid)
            self.inventory.set_variable(container_name, 'container_name', container.image)
            self.inventory.set_variable(container_name, 'container_image', container.image)
            if container.state.running:
                self.inventory.set_variable(container_name, 'container_state', 'Running')
            if container.state.terminated:
                self.inventory.set_variable(container_name, 'container_state', 'Terminated')
            if container.state.waiting:
                self.inventory.set_variable(container_name, 'container_state', 'Waiting')
            self.inventory.set_variable(container_name, 'container_ready', container.ready)
            self.inventory.set_variable(container_name, 'ansible_connection', self.transport)
            self.inventory.set_variable(container_name, 'ansible_{0}_pod'.format(self.transport), pod_name)
            self.inventory.set_variable(container_name, 'ansible_{0}_container'.format(self.transport), container.name)
def create_update_containerinstance(self):
    '\n        Creates or updates a container service with the specified configuration of orchestrator, masters, and agents.\n\n        :return: deserialized container instance state dictionary\n        '
    self.log('Creating / Updating the container instance {0}'.format(self.name))
    registry_credentials = None
    if (self.registry_login_server is not None):
        registry_credentials = [self.cgmodels.ImageRegistryCredential(server=self.registry_login_server, username=self.registry_username, password=self.registry_password)]
    ip_address = None
    if (self.ip_address == 'public'):
        if self.ports:
            ports = []
            for port in self.ports:
                ports.append(self.cgmodels.Port(port=port, protocol='TCP'))
            ip_address = self.cgmodels.IpAddress(ports=ports, ip=self.ip_address)
    containers = []
    for container_def in self.containers:
        name = container_def.get('name')
        image = container_def.get('image')
        memory = container_def.get('memory', 1.5)
        cpu = container_def.get('cpu', 1)
        ports = []
        port_list = container_def.get('ports')
        if port_list:
            for port in port_list:
                ports.append(self.cgmodels.ContainerPort(port=port))
        containers.append(self.cgmodels.Container(name=name, image=image, resources=self.cgmodels.ResourceRequirements(requests=self.cgmodels.ResourceRequests(memory_in_gb=memory, cpu=cpu)), ports=ports))
    parameters = self.cgmodels.ContainerGroup(location=self.location, containers=containers, image_registry_credentials=registry_credentials, restart_policy=None, ip_address=ip_address, os_type=self.os_type, volumes=None, tags=self.tags)
    response = self.containerinstance_client.container_groups.create_or_update(resource_group_name=self.resource_group, container_group_name=self.name, container_group=parameters)
    if isinstance(response, AzureOperationPoller):
        response = self.get_poller_result(response)
    return response.as_dict()
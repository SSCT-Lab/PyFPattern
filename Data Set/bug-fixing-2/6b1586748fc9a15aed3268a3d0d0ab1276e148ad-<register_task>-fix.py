

def register_task(self, family, container_definitions, volumes):
    validated_containers = []
    for container in container_definitions:
        for param in ('memory', 'cpu', 'memoryReservation'):
            if (param in container):
                container[param] = int(container[param])
        if ('portMappings' in container):
            for port_mapping in container['portMappings']:
                for port in ('hostPort', 'containerPort'):
                    if (port in port_mapping):
                        port_mapping[port] = int(port_mapping[port])
        validated_containers.append(container)
    response = self.ecs.register_task_definition(family=family, containerDefinitions=validated_containers, volumes=volumes)
    return response['taskDefinition']

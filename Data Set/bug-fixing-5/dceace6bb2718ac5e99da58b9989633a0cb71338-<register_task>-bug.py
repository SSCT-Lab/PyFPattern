def register_task(self, family, task_role_arn, network_mode, container_definitions, volumes):
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
    try:
        response = self.ecs.register_task_definition(family=family, taskRoleArn=task_role_arn, networkMode=network_mode, containerDefinitions=container_definitions, volumes=volumes)
    except botocore.exceptions.ClientError as e:
        self.module.fail_json(msg=e.message, **camel_dict_to_snake_dict(e.response))
    return response['taskDefinition']
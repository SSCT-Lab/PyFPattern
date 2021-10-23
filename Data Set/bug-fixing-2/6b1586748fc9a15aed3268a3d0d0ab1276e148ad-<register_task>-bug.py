

def register_task(self, family, container_definitions, volumes):
    response = self.ecs.register_task_definition(family=family, containerDefinitions=container_definitions, volumes=volumes)
    return response['taskDefinition']

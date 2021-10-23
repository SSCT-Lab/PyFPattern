def _get_failed_nested_operations(self, current_operations):
    new_operations = []
    for operation in current_operations:
        if (operation.properties.provisioning_state == 'Failed'):
            new_operations.append(operation)
            if (operation.properties.target_resource and ('Microsoft.Resources/deployments' in operation.properties.target_resource.id)):
                nested_deployment = operation.properties.target_resource.resource_name
                try:
                    nested_operations = self.rm_client.deployment_operations.list(self.resource_group_name, nested_deployment)
                except CloudError as exc:
                    self.fail(('List nested deployment operations failed with status code: %s and message: %s' % (exc.status_code, exc.message)))
                new_nested_operations = self._get_failed_nested_operations(nested_operations)
                new_operations += new_nested_operations
    return new_operations
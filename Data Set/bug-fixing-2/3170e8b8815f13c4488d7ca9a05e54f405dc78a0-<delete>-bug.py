

def delete(self):
    try:
        poller = self.network_client.network_security_groups.delete(resource_group_name=self.resource_group, network_security_group_name=self.name)
        result = self.get_poller_result(poller)
    except CloudError as exc:
        raise Exception('Error deleting security group {0} - {1}'.format(self.name, str(exc)))
    return result

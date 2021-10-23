def compare_subnets(self):
    '\n        Compare user subnets with current ELB subnets\n\n        :return: bool True if they match otherwise False\n        '
    subnet_id_list = []
    subnets = []
    if (self.subnets is not None):
        subnets = self.subnets
    if (self.subnet_mappings is not None):
        subnets_from_mappings = []
        for subnet_mapping in self.subnet_mappings:
            subnets.append(subnet_mapping['SubnetId'])
    for subnet in self.elb['AvailabilityZones']:
        subnet_id_list.append(subnet['SubnetId'])
    if (set(subnet_id_list) != set(subnets)):
        return False
    else:
        return True
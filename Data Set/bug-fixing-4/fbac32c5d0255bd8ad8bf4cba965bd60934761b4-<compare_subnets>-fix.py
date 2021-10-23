def compare_subnets(self):
    '\n        Compare user subnets with current ELB subnets\n\n        :return: bool True if they match otherwise False\n        '
    subnet_mapping_id_list = []
    subnet_mappings = []
    if (self.subnets is not None):
        for subnet in self.subnets:
            subnet_mappings.append({
                'SubnetId': subnet,
            })
    if (self.subnet_mappings is not None):
        subnet_mappings = self.subnet_mappings
    for subnet in self.elb['AvailabilityZones']:
        this_mapping = {
            'SubnetId': subnet['SubnetId'],
        }
        for address in subnet['LoadBalancerAddresses']:
            if ('AllocationId' in address):
                this_mapping['AllocationId'] = address['AllocationId']
                break
        subnet_mapping_id_list.append(this_mapping)
    return (set((frozenset(mapping.items()) for mapping in subnet_mapping_id_list)) == set((frozenset(mapping.items()) for mapping in subnet_mappings)))
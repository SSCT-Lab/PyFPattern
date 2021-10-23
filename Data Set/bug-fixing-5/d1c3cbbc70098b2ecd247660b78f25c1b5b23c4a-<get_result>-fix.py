def get_result(self, instance):
    super(AnsibleCloudStackInstance, self).get_result(instance)
    if instance:
        self.result['user_data'] = self._get_instance_user_data(instance)
        if ('securitygroup' in instance):
            security_groups = []
            for securitygroup in instance['securitygroup']:
                security_groups.append(securitygroup['name'])
            self.result['security_groups'] = security_groups
        if ('affinitygroup' in instance):
            affinity_groups = []
            for affinitygroup in instance['affinitygroup']:
                affinity_groups.append(affinitygroup['name'])
            self.result['affinity_groups'] = affinity_groups
        if ('nic' in instance):
            for nic in instance['nic']:
                if (nic['isdefault'] and ('ipaddress' in nic)):
                    self.result['default_ip'] = nic['ipaddress']
    return self.result
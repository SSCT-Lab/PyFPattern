

def get_instance(self):
    instance = self.instance
    if (not instance):
        instance_name = self.get_or_fallback('name', 'display_name')
        vpc_id = self.get_vpc(key='id')
        args = {
            'account': self.get_account(key='name'),
            'domainid': self.get_domain(key='id'),
            'projectid': self.get_project(key='id'),
            'vpcid': vpc_id,
        }
        instances = self.cs.listVirtualMachines(**args)
        if instances:
            for v in instances['virtualmachine']:
                if ((not vpc_id) and self.is_vm_in_vpc(vm=v)):
                    continue
                if (instance_name.lower() in [v['name'].lower(), v['displayname'].lower(), v['id']]):
                    self.instance = v
                    break
    return self.instance

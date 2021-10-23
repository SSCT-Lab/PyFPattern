

def __init__(self, args):
    '\n        :type args: TestConfig\n        '
    super(VcenterProvider, self).__init__(args, config_extension='.ini')
    self.image = 'ansible/ansible:vcenter-simulator@sha256:1a92e84f477ae4c45f9070a5419a0fc2b46abaecdb5bc396826741bca65ce028'
    self.container_name = ''



def __init__(self, args):
    '\n        :type args: TestConfig\n        '
    super(VcenterProvider, self).__init__(args, config_extension='.ini')
    self.image = 'quay.io/ansible/vcenter-test-container:1.0.1'
    self.container_name = ''

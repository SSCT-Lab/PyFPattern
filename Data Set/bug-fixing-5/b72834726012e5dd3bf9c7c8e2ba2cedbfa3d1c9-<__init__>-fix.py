def __init__(self, argument_spec):
    self.spec = argument_spec
    self.module = None
    self.__init_module__()
    self.session_name = self.module.params['session_name']
    self.create_type = self.module.params['create_type']
    self.addr_type = self.module.params['addr_type']
    self.out_if_name = self.module.params['out_if_name']
    self.dest_addr = self.module.params['dest_addr']
    self.src_addr = self.module.params['src_addr']
    self.vrf_name = self.module.params['vrf_name']
    self.use_default_ip = self.module.params['use_default_ip']
    self.state = self.module.params['state']
    self.local_discr = self.module.params['local_discr']
    self.remote_discr = self.module.params['remote_discr']
    self.host = self.module.params['host']
    self.username = self.module.params['username']
    self.port = self.module.params['port']
    self.changed = False
    self.bfd_dict = dict()
    self.updates_cmd = list()
    self.commands = list()
    self.results = dict()
    self.proposed = dict()
    self.existing = dict()
    self.end_state = dict()
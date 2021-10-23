def __init__(self, module):
    if (not has_lib_cs):
        module.fail_json(msg='python library cs required: pip install cs')
    self.result = {
        'changed': False,
    }
    self.common_returns = {
        'id': 'id',
        'name': 'name',
        'created': 'created',
        'zonename': 'zone',
        'state': 'state',
        'project': 'project',
        'account': 'account',
        'domain': 'domain',
        'displaytext': 'display_text',
        'displayname': 'display_name',
        'description': 'description',
    }
    self.returns = {
        
    }
    self.returns_to_int = {
        
    }
    self.case_sensitive_keys = ['id', 'displaytext', 'displayname', 'description']
    self.module = module
    self._connect()
    self.domain = None
    self.account = None
    self.project = None
    self.ip_address = None
    self.network = None
    self.vpc = None
    self.zone = None
    self.vm = None
    self.vm_default_nic = None
    self.os_type = None
    self.hypervisor = None
    self.capabilities = None
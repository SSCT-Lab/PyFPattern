def __init__(self):
    self.module_arg_spec = dict(resource_group=dict(type='str', required=True), name=dict(type='str', required=True), state=dict(choices=['present', 'absent'], default='present', type='str'), location=dict(type='str'), short_hostname=dict(type='str'), vm_size=dict(type='str', choices=[], default='Standard_D1'), admin_username=dict(type='str'), admin_password=dict(type='str', no_log=True), ssh_password_enabled=dict(type='bool', default=True), ssh_public_keys=dict(type='list'), image=dict(type='dict'), storage_account_name=dict(type='str', aliases=['storage_account']), storage_container_name=dict(type='str', aliases=['storage_container'], default='vhds'), storage_blob_name=dict(type='str', aliases=['storage_blob']), os_disk_caching=dict(type='str', aliases=['disk_caching'], choices=['ReadOnly', 'ReadWrite'], default='ReadOnly'), os_type=dict(type='str', choices=['Linux', 'Windows'], default='Linux'), public_ip_allocation_method=dict(type='str', choices=['Dynamic', 'Static'], default='Static', aliases=['public_ip_allocation']), open_ports=dict(type='list'), network_interface_names=dict(type='list', aliases=['network_interfaces']), remove_on_absent=dict(type='list', default=['all']), virtual_network_name=dict(type='str', aliases=['virtual_network']), subnet_name=dict(type='str', aliases=['subnet']), allocated=dict(type='bool', default=True), restarted=dict(type='bool', default=False), started=dict(type='bool', default=True))
    for key in VirtualMachineSizeTypes:
        self.module_arg_spec['vm_size']['choices'].append(getattr(key, 'value'))
    self.resource_group = None
    self.name = None
    self.state = None
    self.location = None
    self.short_hostname = None
    self.vm_size = None
    self.admin_username = None
    self.admin_password = None
    self.ssh_password_enabled = None
    self.ssh_public_keys = None
    self.image = None
    self.storage_account_name = None
    self.storage_container_name = None
    self.storage_blob_name = None
    self.os_type = None
    self.os_disk_caching = None
    self.network_interface_names = None
    self.remove_on_absent = set()
    self.tags = None
    self.force = None
    self.public_ip_allocation_method = None
    self.open_ports = None
    self.virtual_network_name = None
    self.subnet_name = None
    self.allocated = None
    self.restarted = None
    self.started = None
    self.differences = None
    self.results = dict(changed=False, actions=[], powerstate_change=None, ansible_facts=dict(azure_vm=None))
    super(AzureRMVirtualMachine, self).__init__(derived_arg_spec=self.module_arg_spec, supports_check_mode=True)
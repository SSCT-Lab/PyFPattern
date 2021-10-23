def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(datacenter_name=dict(type='str', required=True, aliases=['datacenter']), cluster_name=dict(type='str', aliases=['cluster']), esxi_hostname=dict(type='str', required=True), esxi_username=dict(type='str'), esxi_password=dict(type='str', no_log=True), esxi_ssl_thumbprint=dict(type='str', default=''), state=dict(default='present', choices=['present', 'absent', 'add_or_reconnect', 'reconnect'], type='str'), folder=dict(type='str'), add_connected=dict(type='bool', default=True))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'present', ['esxi_username', 'esxi_password']], ['state', 'add_or_reconnect', ['esxi_username', 'esxi_password']]], required_one_of=[['cluster_name', 'folder']], mutually_exclusive=[['cluster_name', 'folder']])
    vmware_host = VMwareHost(module)
    vmware_host.process_state()
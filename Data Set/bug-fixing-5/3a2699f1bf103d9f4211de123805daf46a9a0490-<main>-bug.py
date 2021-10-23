def main():
    module = AnsibleModule(argument_spec=dict(state=dict(choices=['present', 'absent'], default='present'), name=dict(require=True, aliases=['base_name']), size=dict(default='f1-micro'), source=dict(), image=dict(), image_family=dict(default='debian-8'), disk_type=dict(choices=['pd-standard', 'pd-ssd'], default='pd-standard', type='str'), disk_auto_delete=dict(type='bool', default=True), network=dict(default='default'), subnetwork=dict(), can_ip_forward=dict(type='bool', default=False), external_ip=dict(default='ephemeral'), service_account_email=dict(), service_account_permissions=dict(type='list'), automatic_restart=dict(type='bool', default=None), preemptible=dict(type='bool', default=None), tags=dict(type='list'), metadata=dict(), description=dict(), disks=dict(type='list'), nic_gce_struct=dict(type='list'), project_id=dict(), pem_file=dict(type='path'), credentials_file=dict(type='path')), mutually_exclusive=[['source', 'image']], required_one_of=[['image', 'image_family']], supports_check_mode=True)
    if (not HAS_PYTHON26):
        module.fail_json(msg="GCE module requires python's 'ast' module, python v2.6+")
    if (not HAS_LIBCLOUD):
        module.fail_json(msg='libcloud with GCE support (0.17.0+) required for this module')
    try:
        gce = gce_connect(module)
    except GoogleBaseError as err:
        module.fail_json(msg='GCE Connexion failed')
    if module.check_mode:
        (changed, output) = check_if_system_state_would_be_changed(module, gce)
        module.exit_json(changed=changed, msg=output)
    else:
        module_controller(module, gce)
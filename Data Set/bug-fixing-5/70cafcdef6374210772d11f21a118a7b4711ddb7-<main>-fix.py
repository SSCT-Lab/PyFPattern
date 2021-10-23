def main():
    module = AnsibleModule(argument_spec=dict(api_host=dict(required=True), api_user=dict(required=True), api_password=dict(no_log=True), validate_certs=dict(type='bool', default='no'), node=dict(), src=dict(type='path'), template=dict(), content_type=dict(default='vztmpl', choices=['vztmpl', 'iso']), storage=dict(default='local'), timeout=dict(type='int', default=30), force=dict(type='bool', default='no'), state=dict(default='present', choices=['present', 'absent'])))
    if (not HAS_PROXMOXER):
        module.fail_json(msg='proxmoxer required for this module')
    state = module.params['state']
    api_user = module.params['api_user']
    api_host = module.params['api_host']
    api_password = module.params['api_password']
    validate_certs = module.params['validate_certs']
    node = module.params['node']
    storage = module.params['storage']
    timeout = module.params['timeout']
    if (not api_password):
        try:
            api_password = os.environ['PROXMOX_PASSWORD']
        except KeyError as e:
            module.fail_json(msg='You should set api_password param or use PROXMOX_PASSWORD environment variable')
    try:
        proxmox = ProxmoxAPI(api_host, user=api_user, password=api_password, verify_ssl=validate_certs)
    except Exception as e:
        module.fail_json(msg=('authorization on proxmox cluster failed with exception: %s' % e))
    if (state == 'present'):
        try:
            content_type = module.params['content_type']
            src = module.params['src']
            template = os.path.basename(src)
            if (get_template(proxmox, node, storage, content_type, template) and (not module.params['force'])):
                module.exit_json(changed=False, msg=('template with volid=%s:%s/%s is already exists' % (storage, content_type, template)))
            elif (not src):
                module.fail_json(msg='src param to uploading template file is mandatory')
            elif (not (os.path.exists(src) and os.path.isfile(src))):
                module.fail_json(msg=('template file on path %s not exists' % src))
            if upload_template(module, proxmox, api_host, node, storage, content_type, src, timeout):
                module.exit_json(changed=True, msg=('template with volid=%s:%s/%s uploaded' % (storage, content_type, template)))
        except Exception as e:
            module.fail_json(msg=('uploading of template %s failed with exception: %s' % (template, e)))
    elif (state == 'absent'):
        try:
            content_type = module.params['content_type']
            template = module.params['template']
            if (not template):
                module.fail_json(msg='template param is mandatory')
            elif (not get_template(proxmox, node, storage, content_type, template)):
                module.exit_json(changed=False, msg=('template with volid=%s:%s/%s is already deleted' % (storage, content_type, template)))
            if delete_template(module, proxmox, node, storage, content_type, template, timeout):
                module.exit_json(changed=True, msg=('template with volid=%s:%s/%s deleted' % (storage, content_type, template)))
        except Exception as e:
            module.fail_json(msg=('deleting of template %s failed with exception: %s' % (template, e)))
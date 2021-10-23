

def main():
    argument_spec = purefa_argument_spec()
    argument_spec.update(dict(address=dict(type='str', required=True), enabled=dict(type='bool', default=True), state=dict(type='str', default='present', choices=['absent', 'present'])))
    module = AnsibleModule(argument_spec, supports_check_mode=True)
    pattern = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$')
    if (not pattern.match(module.params['address'])):
        module.fail_json(msg='Valid email address not provided.')
    array = get_system(module)
    exists = False
    try:
        emails = array.list_alert_recipients()
    except Exception:
        module.fail_json(msg='Failed to get existing email list')
    for email in range(0, len(emails)):
        if (emails[email]['name'] == module.params['address']):
            exists = True
            enabled = emails[email]['enabled']
            break
    if ((module.params['state'] == 'present') and (not exists)):
        create_alert(module, array)
    elif ((module.params['state'] == 'present') and exists and (not enabled) and module.params['enabled']):
        enable_alert(module, array)
    elif ((module.params['state'] == 'present') and exists and enabled):
        disable_alert(module, array)
    elif ((module.params['state'] == 'absent') and exists):
        delete_alert(module, array)
    module.exit_json(changed=False)

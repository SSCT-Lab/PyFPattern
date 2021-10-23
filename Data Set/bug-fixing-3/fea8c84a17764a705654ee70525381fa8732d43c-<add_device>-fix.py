def add_device():
    device_ip = get_ip()
    device = get_device(device_ip)
    if device:
        module.exit_json(changed=False, device=device)
    if module.check_mode:
        device = dict(model_handle=None, address=device_ip, landscape=('0x%x' % int(module.params.get('landscape'), 16)))
        module.exit_json(changed=True, device=device)
    resource = ((('model?ipaddress=' + device_ip) + '&commstring=') + module.params.get('community'))
    resource += ('&landscapeid=' + module.params.get('landscape'))
    if module.params.get('agentport', None):
        resource += ('&agentport=' + str(module.params.get('agentport', 161)))
    result = post(resource)
    root = ET.fromstring(result)
    if (root.get('error') != 'Success'):
        module.fail_json(msg=root.get('error-message'))
    namespace = dict(ca='http://www.ca.com/spectrum/restful/schema/response')
    model = root.find('ca:model', namespace)
    model_handle = model.get('mh')
    model_landscape = ('0x%x' % int(((int(model_handle, 16) // 1048576) * 1048576)))
    device = dict(model_handle=model_handle, address=device_ip, landscape=model_landscape)
    module.exit_json(changed=True, device=device)
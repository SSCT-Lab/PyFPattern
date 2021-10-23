def main():
    fields = {
        'api_url': {
            'required': False,
            'type': 'str',
        },
        'api_username': {
            'required': False,
            'type': 'str',
        },
        'api_password': {
            'required': False,
            'type': 'str',
            'no_log': True,
        },
        'instance_ids': {
            'required': False,
            'aliases': ['ids'],
            'type': 'list',
        },
        'template_name': {
            'required': False,
            'type': 'str',
        },
        'template_id': {
            'required': False,
            'type': 'int',
        },
        'state': {
            'default': 'present',
            'choices': ['present', 'absent', 'rebooted', 'poweredoff', 'running'],
            'type': 'str',
        },
        'mode': {
            'required': False,
            'type': 'str',
        },
        'owner_id': {
            'required': False,
            'type': 'int',
        },
        'group_id': {
            'required': False,
            'type': 'int',
        },
        'wait': {
            'default': True,
            'type': 'bool',
        },
        'wait_timeout': {
            'default': 300,
            'type': 'int',
        },
        'hard': {
            'default': False,
            'type': 'bool',
        },
        'memory': {
            'required': False,
            'type': 'str',
        },
        'cpu': {
            'required': False,
            'type': 'float',
        },
        'vcpu': {
            'required': False,
            'type': 'int',
        },
        'disk_size': {
            'required': False,
            'type': 'str',
        },
        'networks': {
            'default': [],
            'type': 'list',
        },
        'count': {
            'default': 1,
            'type': 'int',
        },
        'exact_count': {
            'required': False,
            'type': 'int',
        },
        'attributes': {
            'default': {
                
            },
            'type': 'dict',
        },
        'count_attributes': {
            'required': False,
            'type': 'dict',
        },
        'labels': {
            'default': [],
            'type': 'list',
        },
        'count_labels': {
            'required': False,
            'type': 'list',
        },
        'disk_saveas': {
            'type': 'dict',
        },
    }
    module = AnsibleModule(argument_spec=fields, mutually_exclusive=[['template_id', 'template_name', 'instance_ids'], ['template_id', 'template_name', 'disk_saveas'], ['instance_ids', 'count_attributes', 'count'], ['instance_ids', 'count_labels', 'count'], ['instance_ids', 'exact_count'], ['instance_ids', 'attributes'], ['instance_ids', 'labels'], ['disk_saveas', 'attributes'], ['disk_saveas', 'labels'], ['exact_count', 'count'], ['count', 'hard'], ['instance_ids', 'cpu'], ['instance_ids', 'vcpu'], ['instance_ids', 'memory'], ['instance_ids', 'disk_size'], ['instance_ids', 'networks']], supports_check_mode=True)
    if (not HAS_OCA):
        module.fail_json(msg='This module requires python-oca to work!')
    auth = get_connection_info(module)
    params = module.params
    instance_ids = params.get('instance_ids')
    requested_template_name = params.get('template_name')
    requested_template_id = params.get('template_id')
    state = params.get('state')
    permissions = params.get('mode')
    owner_id = params.get('owner_id')
    group_id = params.get('group_id')
    wait = params.get('wait')
    wait_timeout = params.get('wait_timeout')
    hard = params.get('hard')
    memory = params.get('memory')
    cpu = params.get('cpu')
    vcpu = params.get('vcpu')
    disk_size = params.get('disk_size')
    networks = params.get('networks')
    count = params.get('count')
    exact_count = params.get('exact_count')
    attributes = params.get('attributes')
    count_attributes = params.get('count_attributes')
    labels = params.get('labels')
    count_labels = params.get('count_labels')
    disk_saveas = params.get('disk_saveas')
    client = oca.Client(((auth.username + ':') + auth.password), auth.url)
    if attributes:
        attributes = dict(((key.upper(), value) for (key, value) in attributes.items()))
        check_attributes(module, attributes)
    if count_attributes:
        count_attributes = dict(((key.upper(), value) for (key, value) in count_attributes.items()))
        if (not attributes):
            import copy
            module.warn('When you pass `count_attributes` without `attributes` option when deploying, `attributes` option will have same values implicitly.')
            attributes = copy.copy(count_attributes)
        check_attributes(module, count_attributes)
    if (count_labels and (not labels)):
        module.warn('When you pass `count_labels` without `labels` option when deploying, `labels` option will have same values implicitly.')
        labels = count_labels
    template_id = None
    if (requested_template_id or requested_template_name):
        template_id = get_template_id(module, client, requested_template_id, requested_template_name)
        if (not template_id):
            if requested_template_id:
                module.fail_json(msg=('There is no template with template_id: ' + str(requested_template_id)))
            elif requested_template_name:
                module.fail_json(msg=('There is no template with name: ' + requested_template_name))
    if (exact_count and (not template_id)):
        module.fail_json(msg='Option `exact_count` needs template_id or template_name')
    if ((exact_count is not None) and (not (count_attributes or count_labels))):
        module.fail_json(msg='Either `count_attributes` or `count_labels` has to be specified with option `exact_count`.')
    if ((count_attributes or count_labels) and (exact_count is None)):
        module.fail_json(msg='Option `exact_count` has to be specified when either `count_attributes` or `count_labels` is used.')
    if (template_id and (state != 'present')):
        module.fail_json(msg="Only state 'present' is valid for the template")
    if memory:
        attributes['MEMORY'] = str(int(get_size_in_MB(module, memory)))
    if cpu:
        attributes['CPU'] = str(cpu)
    if vcpu:
        attributes['VCPU'] = str(vcpu)
    if ((exact_count is not None) and (state != 'present')):
        module.fail_json(msg='The `exact_count` option is valid only for the `present` state')
    if ((exact_count is not None) and (exact_count < 0)):
        module.fail_json(msg='`exact_count` cannot be less than 0')
    if (count <= 0):
        module.fail_json(msg='`count` has to be grater than 0')
    if (permissions is not None):
        import re
        if (re.match('^[0-7]{3}$', permissions) is None):
            module.fail_json(msg='Option `mode` has to have exactly 3 digits and be in the octet format e.g. 600')
    if (exact_count is not None):
        (changed, instances_list, tagged_instances_list) = create_exact_count_of_vms(module, client, template_id, exact_count, attributes, count_attributes, labels, count_labels, disk_size, networks, hard, wait, wait_timeout)
        vms = tagged_instances_list
    elif (template_id and (state == 'present')):
        (changed, instances_list, tagged_instances_list) = create_count_of_vms(module, client, template_id, count, attributes, labels, disk_size, networks, wait, wait_timeout)
        vms = instances_list
    else:
        if (not (instance_ids or attributes or labels)):
            module.fail_json(msg='At least one of `instance_ids`,`attributes`,`labels` must be passed!')
        if (memory or cpu or vcpu or disk_size or networks):
            module.fail_json(msg='Parameters as `memory`, `cpu`, `vcpu`, `disk_size` and `networks` you can only set when deploying a VM!')
        if (hard and (state not in ['rebooted', 'poweredoff', 'absent', 'present'])):
            module.fail_json(msg="The 'hard' option can be used only for one of these states: 'rebooted', 'poweredoff', 'absent' and 'present'")
        vms = []
        tagged = False
        changed = False
        if instance_ids:
            vms = get_vms_by_ids(module, client, state, instance_ids)
        else:
            tagged = True
            vms = get_all_vms_by_attributes(client, attributes, labels)
        if ((len(vms) == 0) and (state != 'absent') and (state != 'present')):
            module.fail_json(msg='There are no instances with specified `instance_ids`, `attributes` and/or `labels`')
        if ((len(vms) == 0) and (state == 'present') and (not tagged)):
            module.fail_json(msg='There are no instances with specified `instance_ids`.')
        if (tagged and (state == 'absent')):
            module.fail_json(msg='Option `instance_ids` is required when state is `absent`.')
        if (state == 'absent'):
            changed = terminate_vms(module, client, vms, hard)
        elif (state == 'rebooted'):
            changed = reboot_vms(module, client, vms, wait_timeout, hard)
        elif (state == 'poweredoff'):
            changed = poweroff_vms(module, client, vms, hard)
        elif (state == 'running'):
            changed = resume_vms(module, client, vms)
        instances_list = vms
        tagged_instances_list = []
    if (permissions is not None):
        changed = (set_vm_permissions(module, client, vms, permissions) or changed)
    if ((owner_id is not None) or (group_id is not None)):
        changed = (set_vm_ownership(module, client, vms, owner_id, group_id) or changed)
    if (wait and (not module.check_mode) and (state != 'present')):
        wait_for = {
            'absent': wait_for_done,
            'rebooted': wait_for_running,
            'poweredoff': wait_for_poweroff,
            'running': wait_for_running,
        }
        for vm in vms:
            if (vm is not None):
                wait_for[state](module, vm, wait_timeout)
    if (disk_saveas is not None):
        if (len(vms) == 0):
            module.fail_json(msg='There is no VM whose disk will be saved.')
        disk_save_as(module, client, vms[0], disk_saveas, wait_timeout)
        changed = True
    instances = list((get_vm_info(client, vm) for vm in instances_list if (vm is not None)))
    instances_ids = list((vm.id for vm in instances_list if (vm is not None)))
    tagged_instances = list((get_vm_info(client, vm) for vm in tagged_instances_list if (vm is not None)))
    result = {
        'changed': changed,
        'instances': instances,
        'instances_ids': instances_ids,
        'tagged_instances': tagged_instances,
    }
    module.exit_json(**result)
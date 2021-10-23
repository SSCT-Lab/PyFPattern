

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(resource=dict(required=True), tags=dict(type='dict'), state=dict(default='present', choices=['present', 'absent', 'list'])))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    resource = module.params.get('resource')
    tags = module.params.get('tags')
    state = module.params.get('state')
    ec2 = ec2_connect(module)
    filters = {
        'resource-id': resource,
    }
    gettags = ec2.get_all_tags(filters=filters)
    dictadd = {
        
    }
    dictremove = {
        
    }
    baddict = {
        
    }
    tagdict = {
        
    }
    for tag in gettags:
        tagdict[tag.name] = tag.value
    if (state == 'present'):
        if (not tags):
            module.fail_json(msg='tags argument is required when state is present')
        if set(tags.items()).issubset(set(tagdict.items())):
            module.exit_json(msg=('Tags already exists in %s.' % resource), changed=False)
        else:
            for (key, value) in set(tags.items()):
                if ((key, value) not in set(tagdict.items())):
                    dictadd[key] = value
        if (not module.check_mode):
            ec2.create_tags(resource, dictadd)
        module.exit_json(msg=('Tags %s created for resource %s.' % (dictadd, resource)), changed=True)
    if (state == 'absent'):
        if (not tags):
            module.fail_json(msg='tags argument is required when state is absent')
        for (key, value) in set(tags.items()):
            if ((key, value) not in set(tagdict.items())):
                baddict[key] = value
                if (set(baddict) == set(tags)):
                    module.exit_json(msg='Nothing to remove here. Move along.', changed=False)
        for (key, value) in set(tags.items()):
            if ((key, value) in set(tagdict.items())):
                dictremove[key] = value
        if (not module.check_mode):
            ec2.delete_tags(resource, dictremove)
        module.exit_json(msg=('Tags %s removed for resource %s.' % (dictremove, resource)), changed=True)
    if (state == 'list'):
        module.exit_json(changed=False, tags=tagdict)

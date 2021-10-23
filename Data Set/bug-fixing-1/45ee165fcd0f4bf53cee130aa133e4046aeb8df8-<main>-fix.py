

def main():
    argument_spec = openstack_full_argument_spec(name=dict(required=True), metadata=dict(required=False, default=None, type='dict'), availability_zone=dict(required=False, default=None), hosts=dict(required=False, default=None, type='list'), state=dict(default='present', choices=['absent', 'present']))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, supports_check_mode=True, **module_kwargs)
    name = module.params['name']
    metadata = module.params['metadata']
    availability_zone = module.params['availability_zone']
    hosts = module.params['hosts']
    state = module.params['state']
    if (metadata is not None):
        metadata.pop('availability_zone', None)
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        aggregates = cloud.search_aggregates(name_or_id=name)
        if (len(aggregates) == 1):
            aggregate = aggregates[0]
        elif (len(aggregates) == 0):
            aggregate = None
        else:
            raise Exception('Should not happen')
        if module.check_mode:
            module.exit_json(changed=_system_state_change(module, aggregate))
        if (state == 'present'):
            if (aggregate is None):
                aggregate = cloud.create_aggregate(name=name, availability_zone=availability_zone)
                if hosts:
                    for h in hosts:
                        cloud.add_host_to_aggregate(aggregate.id, h)
                if metadata:
                    cloud.set_aggregate_metadata(aggregate.id, metadata)
                changed = True
            elif _needs_update(module, aggregate):
                if (availability_zone is not None):
                    aggregate = cloud.update_aggregate(aggregate.id, name=name, availability_zone=availability_zone)
                if (metadata is not None):
                    metas = metadata
                    for i in (set(aggregate.metadata.keys()) - set(metadata.keys())):
                        if (i != 'availability_zone'):
                            metas[i] = None
                    cloud.set_aggregate_metadata(aggregate.id, metas)
                if (hosts is not None):
                    for i in (set(aggregate.hosts) - set(hosts)):
                        cloud.remove_host_from_aggregate(aggregate.id, i)
                    for i in (set(hosts) - set(aggregate.hosts)):
                        cloud.add_host_to_aggregate(aggregate.id, i)
                changed = True
            else:
                changed = False
            module.exit_json(changed=changed)
        elif (state == 'absent'):
            if (aggregate is None):
                changed = False
            else:
                if hosts:
                    for h in hosts:
                        cloud.remove_host_from_aggregate(aggregate.id, h)
                cloud.delete_aggregate(aggregate.id)
                changed = True
            module.exit_json(changed=changed)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))

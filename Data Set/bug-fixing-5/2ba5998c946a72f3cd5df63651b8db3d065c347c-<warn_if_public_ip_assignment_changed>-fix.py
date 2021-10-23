def warn_if_public_ip_assignment_changed(module, instance):
    assign_public_ip = module.params.get('assign_public_ip')
    public_dns_name = getattr(instance, 'public_dns_name', None)
    if ((assign_public_ip or public_dns_name) and ((not public_dns_name) or (not assign_public_ip))):
        module.warn('Unable to modify public ip assignment to {0} for instance {1}. Whether or not to assign a public IP is determined during instance creation.'.format(assign_public_ip, instance.id))
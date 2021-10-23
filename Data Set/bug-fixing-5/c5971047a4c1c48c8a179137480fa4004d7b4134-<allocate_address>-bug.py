def allocate_address(ec2, domain, reuse_existing_ip_allowed):
    ' Allocate a new elastic IP address (when needed) and return it '
    if reuse_existing_ip_allowed:
        domain_filter = {
            'domain': (domain or 'standard'),
        }
        all_addresses = ec2.get_all_addresses(filters=domain_filter)
        if (domain == 'vpc'):
            unassociated_addresses = [a for a in all_addresses if (not a.association_id)]
        else:
            unassociated_addresses = [a for a in all_addresses if (not a.instance_id)]
        if unassociated_addresses:
            return unassociated_addresses[0]
    return ec2.allocate_address(domain=domain)
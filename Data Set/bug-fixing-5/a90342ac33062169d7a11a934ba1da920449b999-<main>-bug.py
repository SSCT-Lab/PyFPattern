def main():
    argument_spec = dict(name=dict(required=True), cidr_block=dict(type='list', required=True), tenancy=dict(choices=['default', 'dedicated'], default='default'), dns_support=dict(type='bool', default=True), dns_hostnames=dict(type='bool', default=True), dhcp_opts_id=dict(), tags=dict(type='dict', aliases=['resource_tags']), state=dict(choices=['present', 'absent'], default='present'), multi_ok=dict(type='bool', default=False), purge_cidrs=dict(type='bool', default=False))
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)
    name = module.params.get('name')
    cidr_block = module.params.get('cidr_block')
    purge_cidrs = module.params.get('purge_cidrs')
    tenancy = module.params.get('tenancy')
    dns_support = module.params.get('dns_support')
    dns_hostnames = module.params.get('dns_hostnames')
    dhcp_id = module.params.get('dhcp_opts_id')
    tags = module.params.get('tags')
    state = module.params.get('state')
    multi = module.params.get('multi_ok')
    changed = False
    connection = module.client('ec2', retry_decorator=AWSRetry.jittered_backoff(retries=8, delay=3, catch_extra_error_codes=['InvalidVpcID.NotFound']))
    if (dns_hostnames and (not dns_support)):
        module.fail_json(msg='In order to enable DNS Hostnames you must also enable DNS support')
    if (state == 'present'):
        vpc_id = vpc_exists(module, connection, name, cidr_block, multi)
        if (vpc_id is None):
            vpc_id = create_vpc(connection, module, cidr_block[0], tenancy)
            changed = True
        vpc_obj = get_vpc(module, connection, vpc_id)
        associated_cidrs = dict(((cidr['CidrBlock'], cidr['AssociationId']) for cidr in vpc_obj.get('CidrBlockAssociationSet', []) if (cidr['CidrBlockState']['State'] != 'disassociated')))
        to_add = [cidr for cidr in cidr_block if (cidr not in associated_cidrs)]
        to_remove = [associated_cidrs[cidr] for cidr in associated_cidrs if (cidr not in cidr_block)]
        expected_cidrs = ([cidr for cidr in associated_cidrs if (associated_cidrs[cidr] not in to_remove)] + to_add)
        if (len(cidr_block) > 1):
            for cidr in to_add:
                changed = True
                connection.associate_vpc_cidr_block(CidrBlock=cidr, VpcId=vpc_id)
        if purge_cidrs:
            for association_id in to_remove:
                changed = True
                try:
                    connection.disassociate_vpc_cidr_block(AssociationId=association_id)
                except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                    module.fail_json_aws(e, 'Unable to disassociate {0}. You must detach or delete all gateways and resources that are associated with the CIDR block before you can disassociate it.'.format(association_id))
        if (dhcp_id is not None):
            try:
                if update_dhcp_opts(connection, module, vpc_obj, dhcp_id):
                    changed = True
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                module.fail_json_aws(e, 'Failed to update DHCP options')
        if ((tags is not None) or (name is not None)):
            try:
                if update_vpc_tags(connection, module, vpc_id, tags, name):
                    changed = True
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                module.fail_json_aws(e, msg='Failed to update tags')
        current_dns_enabled = connection.describe_vpc_attribute(Attribute='enableDnsSupport', VpcId=vpc_id, aws_retry=True)['EnableDnsSupport']['Value']
        current_dns_hostnames = connection.describe_vpc_attribute(Attribute='enableDnsHostnames', VpcId=vpc_id, aws_retry=True)['EnableDnsHostnames']['Value']
        if (current_dns_enabled != dns_support):
            changed = True
            if (not module.check_mode):
                try:
                    connection.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={
                        'Value': dns_support,
                    })
                except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                    module.fail_json_aws(e, 'Failed to update enabled dns support attribute')
        if (current_dns_hostnames != dns_hostnames):
            changed = True
            if (not module.check_mode):
                try:
                    connection.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={
                        'Value': dns_hostnames,
                    })
                except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                    module.fail_json_aws(e, 'Failed to update enabled dns hostnames attribute')
        if (to_add or to_remove):
            try:
                connection.get_waiter('vpc_available').wait(VpcIds=[vpc_id], Filters=[{
                    'Name': 'cidr-block-association.cidr-block',
                    'Values': expected_cidrs,
                }])
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                module.fail_json_aws(e, 'Failed to wait for CIDRs to update')
        wait_for_vpc_attribute(connection, module, vpc_id, 'enableDnsSupport', dns_support)
        wait_for_vpc_attribute(connection, module, vpc_id, 'enableDnsHostnames', dns_hostnames)
        final_state = camel_dict_to_snake_dict(get_vpc(module, connection, vpc_id))
        final_state['tags'] = boto3_tag_list_to_ansible_dict(final_state.get('tags', []))
        final_state['id'] = final_state.pop('vpc_id')
        module.exit_json(changed=changed, vpc=final_state)
    elif (state == 'absent'):
        vpc_id = vpc_exists(module, connection, name, cidr_block, multi)
        if (vpc_id is not None):
            try:
                if (not module.check_mode):
                    connection.delete_vpc(VpcId=vpc_id)
                changed = True
            except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                module.fail_json_aws(e, msg='Failed to delete VPC {0} You may want to use the ec2_vpc_subnet, ec2_vpc_igw, and/or ec2_vpc_route_table modules to ensure the other components are absent.'.format(vpc_id))
        module.exit_json(changed=changed, vpc={
            
        })
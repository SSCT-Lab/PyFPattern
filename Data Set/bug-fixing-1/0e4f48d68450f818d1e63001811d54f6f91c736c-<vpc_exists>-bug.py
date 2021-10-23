

def vpc_exists(module, vpc, name, cidr_block, multi):
    'Returns True or False in regards to the existence of a VPC. When supplied\n    with a CIDR, it will check for matching tags to determine if it is a match\n    otherwise it will assume the VPC does not exist and thus return false.\n    '
    matched_vpc = None
    try:
        matching_vpcs = vpc.get_all_vpcs(filters={
            'tag:Name': name,
            'cidr-block': cidr_block,
        })
    except Exception as e:
        e_msg = boto_exception(e)
        module.fail_json(msg=e_msg)
    if (len(matching_vpcs) == 1):
        matched_vpc = matching_vpcs[0]
    elif (len(matching_vpcs) > 1):
        if multi:
            module.fail_json(msg=('Currently there are %d VPCs that have the same name and CIDR block you specified. If you would like to create the VPC anyway please pass True to the multi_ok param.' % len(matching_vpcs)))
    return matched_vpc

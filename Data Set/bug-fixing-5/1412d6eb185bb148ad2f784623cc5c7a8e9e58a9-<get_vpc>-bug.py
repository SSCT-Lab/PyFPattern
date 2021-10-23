def get_vpc(module, connection, vpc_id):
    try:
        vpc_obj = connection.describe_vpcs(VpcIds=[vpc_id])['Vpcs'][0]
        classic_link = connection.describe_vpc_classic_link(VpcIds=[vpc_id])['Vpcs'][0].get('ClassicLinkEnabled')
        vpc_obj['ClassicLinkEnabled'] = classic_link
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg='Failed to describe VPCs')
    return vpc_obj
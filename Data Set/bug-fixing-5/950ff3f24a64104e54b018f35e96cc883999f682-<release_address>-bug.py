def release_address(client, allocation_id, check_mode=False):
    'Release an EIP from your EIP Pool\n    Args:\n        client (botocore.client.EC2): Boto3 client\n        allocation_id (str): The eip Amazon identifier.\n\n    Kwargs:\n        check_mode (bool): if set to true, do not run anything and\n            falsify the results.\n\n    Basic Usage:\n        >>> client = boto3.client(\'ec2\')\n        >>> allocation_id = "eipalloc-123456"\n        >>> release_address(client, allocation_id)\n        True\n\n    Returns:\n        Boolean, string\n    '
    err_msg = ''
    if check_mode:
        return (True, '')
    ip_released = False
    params = {
        'AllocationId': allocation_id,
    }
    try:
        client.release_address(**params)
        ip_released = True
    except botocore.exceptions.ClientError as e:
        err_msg = str(e)
    return (ip_released, err_msg)
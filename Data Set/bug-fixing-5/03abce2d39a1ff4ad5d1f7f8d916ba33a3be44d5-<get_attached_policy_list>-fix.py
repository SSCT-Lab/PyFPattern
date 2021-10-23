@AWSRetry.exponential_backoff()
def get_attached_policy_list(connection, module, name):
    try:
        paginator = connection.get_paginator('list_attached_group_policies')
        return paginator.paginate(GroupName=name).build_full_result()['AttachedPolicies']
    except ClientError as e:
        if (e.response['Error']['Code'] == 'NoSuchEntity'):
            return None
        else:
            raise
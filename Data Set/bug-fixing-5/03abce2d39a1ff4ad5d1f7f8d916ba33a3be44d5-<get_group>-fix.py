@AWSRetry.exponential_backoff()
def get_group(connection, module, name):
    try:
        paginator = connection.get_paginator('get_group')
        return paginator.paginate(GroupName=name).build_full_result()
    except ClientError as e:
        if (e.response['Error']['Code'] == 'NoSuchEntity'):
            return None
        else:
            raise
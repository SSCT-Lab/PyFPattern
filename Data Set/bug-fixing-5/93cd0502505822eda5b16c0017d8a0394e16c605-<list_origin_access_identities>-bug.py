def list_origin_access_identities(self):
    try:
        paginator = self.client.get_paginator('list_cloud_front_origin_access_identities')
        result = paginator.paginate().build_full_result()['CloudFrontOriginAccessIdentityList']
        return result.get('Items', [])
    except botocore.exceptions.ClientError as e:
        self.module.fail_json_aws(e, msg='Error listing cloud front origin access identities')
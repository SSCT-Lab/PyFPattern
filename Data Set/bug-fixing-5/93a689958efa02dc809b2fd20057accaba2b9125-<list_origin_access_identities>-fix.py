def list_origin_access_identities(self):
    try:
        func = partial(self.client.list_cloud_front_origin_access_identities)
        origin_access_identity_list = self.paginated_response(func, 'CloudFrontOriginAccessIdentityList')
        if (origin_access_identity_list['Quantity'] > 0):
            return origin_access_identity_list['Items']
        return {
            
        }
    except Exception as e:
        self.module.fail_json(msg=('Error listing cloud front origin access identities - ' + str(e)), exception=traceback.format_exc(e))
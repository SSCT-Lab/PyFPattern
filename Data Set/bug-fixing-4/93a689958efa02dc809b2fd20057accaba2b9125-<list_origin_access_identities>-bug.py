def list_origin_access_identities(self):
    try:
        func = partial(self.client.list_cloud_front_origin_access_identities)
        return self.paginated_response(func, 'CloudFrontOriginAccessIdentityList')['Items']
    except Exception as e:
        self.module.fail_json(msg=('Error listing cloud front origin access identities = ' + str(e)), exception=traceback.format_exc(e))
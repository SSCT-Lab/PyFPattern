def list_distributions_by_web_acl_id(self, web_acl_id):
    try:
        func = partial(self.client.list_distributions_by_web_acl_id, WebAclId=web_acl_id)
        distributions = self.paginated_response(func, 'DistributionList')['Items']
        return self.keyed_list_helper(distributions)
    except Exception as e:
        self.module.fail_json(msg=('Error listing distributions by web acl id = ' + str(e)), exception=traceback.format_exc(e))
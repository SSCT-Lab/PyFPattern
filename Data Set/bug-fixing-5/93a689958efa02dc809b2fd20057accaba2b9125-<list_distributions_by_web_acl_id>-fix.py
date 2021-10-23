def list_distributions_by_web_acl_id(self, web_acl_id):
    try:
        func = partial(self.client.list_distributions_by_web_acl_id, WebAclId=web_acl_id)
        distribution_list = self.paginated_response(func, 'DistributionList')
        if (distribution_list['Quantity'] == 0):
            return {
                
            }
        else:
            distribution_list = distribution_list['Items']
        return self.keyed_list_helper(distribution_list)
    except Exception as e:
        self.module.fail_json(msg=('Error listing distributions by web acl id - ' + str(e)), exception=traceback.format_exc(e))
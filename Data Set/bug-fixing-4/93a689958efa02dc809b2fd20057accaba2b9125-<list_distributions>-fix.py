def list_distributions(self, keyed=True):
    try:
        func = partial(self.client.list_distributions)
        distribution_list = self.paginated_response(func, 'DistributionList')
        if (distribution_list['Quantity'] == 0):
            return {
                
            }
        else:
            distribution_list = distribution_list['Items']
        if (not keyed):
            return distribution_list
        return self.keyed_list_helper(distribution_list)
    except Exception as e:
        self.module.fail_json(msg=('Error listing distributions - ' + str(e)), exception=traceback.format_exc(e))
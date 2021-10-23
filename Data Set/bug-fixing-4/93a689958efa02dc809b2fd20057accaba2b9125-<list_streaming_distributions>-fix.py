def list_streaming_distributions(self, keyed=True):
    try:
        func = partial(self.client.list_streaming_distributions)
        streaming_distribution_list = self.paginated_response(func, 'StreamingDistributionList')
        if (streaming_distribution_list['Quantity'] == 0):
            return {
                
            }
        else:
            streaming_distribution_list = streaming_distribution_list['Items']
        if (not keyed):
            return streaming_distribution_list
        return self.keyed_list_helper(streaming_distribution_list)
    except Exception as e:
        self.module.fail_json(msg=('Error listing streaming distributions - ' + str(e)), exception=traceback.format_exc(e))
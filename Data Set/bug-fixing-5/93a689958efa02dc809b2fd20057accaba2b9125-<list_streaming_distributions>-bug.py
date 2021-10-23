def list_streaming_distributions(self):
    try:
        func = partial(self.client.list_streaming_distributions)
        streaming_distributions = self.paginated_response(func, 'StreamingDistributionList')['Items']
        return self.keyed_list_helper(streaming_distributions)
    except Exception as e:
        self.module.fail_json(msg=('Error listing streaming distributions = ' + str(e)), exception=traceback.format_exc(e))
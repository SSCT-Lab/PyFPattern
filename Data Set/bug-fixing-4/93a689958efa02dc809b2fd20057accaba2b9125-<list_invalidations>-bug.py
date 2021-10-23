def list_invalidations(self, distribution_id):
    try:
        func = partial(self.client.list_invalidations, DistributionId=distribution_id)
        return self.paginated_response(func, 'InvalidationList')['Items']
    except Exception as e:
        self.module.fail_json(msg=('Error listing invalidations = ' + str(e)), exception=traceback.format_exc(e))
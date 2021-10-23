def list_invalidations(self, distribution_id):
    try:
        func = partial(self.client.list_invalidations, DistributionId=distribution_id)
        invalidation_list = self.paginated_response(func, 'InvalidationList')
        if (invalidation_list['Quantity'] > 0):
            return invalidation_list['Items']
        return {
            
        }
    except Exception as e:
        self.module.fail_json(msg=('Error listing invalidations - ' + str(e)), exception=traceback.format_exc(e))
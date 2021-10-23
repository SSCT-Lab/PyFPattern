def get_distribution_config(self, distribution_id):
    try:
        func = partial(self.client.get_distribution_config, Id=distribution_id)
        return self.paginated_response(func)
    except botocore.exceptions.ClientError as e:
        self.module.fail_json(msg=('Error describing distribution configuration - ' + str(e)), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
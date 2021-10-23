def list_keys(module, s3, bucket, prefix, marker, max_keys):
    pagination_params = {
        'Bucket': bucket,
    }
    for (param_name, param_value) in (('Prefix', prefix), ('StartAfter', marker), ('MaxKeys', max_keys)):
        pagination_params[param_name] = param_value
    try:
        keys = [key for key in paginated_list(s3, **pagination_params)]
        module.exit_json(msg='LIST operation complete', s3_keys=keys)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg='Failed while listing the keys in the bucket {0}'.format(bucket), exception=traceback.format_exc(), **camel_dict_to_snake_dict(e.response))
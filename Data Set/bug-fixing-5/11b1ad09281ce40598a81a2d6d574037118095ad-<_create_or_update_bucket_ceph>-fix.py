def _create_or_update_bucket_ceph(connection, module, location):
    name = module.params.get('name')
    changed = False
    try:
        bucket = connection.get_bucket(name)
    except S3ResponseError as e:
        try:
            bucket = connection.create_bucket(name, location=location)
            changed = True
        except (S3CreateError, BotoClientError) as e:
            module.fail_json(msg=e.message)
    if bucket:
        module.exit_json(changed=changed)
    else:
        module.fail_json(msg='Unable to create bucket, no error from the API')
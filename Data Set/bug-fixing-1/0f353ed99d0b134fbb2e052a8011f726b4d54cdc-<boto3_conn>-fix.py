

def boto3_conn(module, conn_type=None, resource=None, region=None, endpoint=None, **params):
    try:
        return _boto3_conn(conn_type=conn_type, resource=resource, region=region, endpoint=endpoint, **params)
    except ValueError as e:
        module.fail_json(msg=("Couldn't connect to AWS: %s" % to_native(e)))
    except (botocore.exceptions.ProfileNotFound, botocore.exceptions.PartialCredentialsError, botocore.exceptions.NoCredentialsError, botocore.exceptions.ConfigParseError) as e:
        module.fail_json(msg=to_native(e))
    except botocore.exceptions.NoRegionError as e:
        module.fail_json(msg=('The %s module requires a region and none was found in configuration, environment variables or module parameters' % module._name))

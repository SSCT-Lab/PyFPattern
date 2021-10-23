def _create_or_update_bucket(connection, module, location):
    policy = module.params.get('policy')
    name = module.params.get('name')
    requester_pays = module.params.get('requester_pays')
    tags = module.params.get('tags')
    versioning = module.params.get('versioning')
    changed = False
    try:
        bucket = connection.get_bucket(name)
    except S3ResponseError as e:
        try:
            bucket = connection.create_bucket(name, location=location)
            changed = True
        except (S3CreateError, BotoClientError) as e:
            module.fail_json(msg=e.message)
    versioning_status = bucket.get_versioning_status()
    if (versioning is not None):
        if (versioning and (versioning_status.get('Versioning') != 'Enabled')):
            try:
                bucket.configure_versioning(versioning)
                changed = True
                versioning_status = bucket.get_versioning_status()
            except S3ResponseError as e:
                module.fail_json(msg=e.message, exception=traceback.format_exc())
        elif ((not versioning) and (versioning_status.get('Versioning') == 'Enabled')):
            try:
                bucket.configure_versioning(versioning)
                changed = True
                versioning_status = bucket.get_versioning_status()
            except S3ResponseError as e:
                module.fail_json(msg=e.message, exception=traceback.format_exc())
    requester_pays_status = get_request_payment_status(bucket)
    if (requester_pays_status != requester_pays):
        if requester_pays:
            payer = 'Requester'
        else:
            payer = 'BucketOwner'
        bucket.set_request_payment(payer=payer)
        changed = True
        requester_pays_status = get_request_payment_status(bucket)
    try:
        current_policy = json.loads(bucket.get_policy())
    except S3ResponseError as e:
        if (e.error_code == 'NoSuchBucketPolicy'):
            current_policy = {
                
            }
        else:
            module.fail_json(msg=e.message)
    if (policy is not None):
        if isinstance(policy, string_types):
            policy = json.loads(policy)
        if (not policy):
            bucket.delete_policy()
            changed = bool(current_policy)
        elif (sort_json_policy_dict(current_policy) != sort_json_policy_dict(policy)):
            changed = compare_policies(sort_json_policy_dict(current_policy), sort_json_policy_dict(policy))
            try:
                if changed:
                    bucket.set_policy(json.dumps(policy))
                current_policy = json.loads(bucket.get_policy())
            except S3ResponseError as e:
                module.fail_json(msg=e.message)
    try:
        current_tags = bucket.get_tags()
    except S3ResponseError as e:
        if (e.error_code == 'NoSuchTagSet'):
            current_tags = None
        else:
            module.fail_json(msg=e.message)
    if (current_tags is None):
        current_tags_dict = {
            
        }
    else:
        current_tags_dict = dict(((t.key, t.value) for t in current_tags[0]))
    if (tags is not None):
        if (current_tags_dict != tags):
            try:
                if tags:
                    bucket.set_tags(create_tags_container(tags))
                else:
                    bucket.delete_tags()
                current_tags_dict = tags
                changed = True
            except S3ResponseError as e:
                module.fail_json(msg=e.message)
    module.exit_json(changed=changed, name=bucket.name, versioning=versioning_status, requester_pays=requester_pays_status, policy=current_policy, tags=current_tags_dict)
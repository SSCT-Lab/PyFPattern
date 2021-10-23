def create_or_update_dynamo_table(connection, module, boto3_dynamodb=None, boto3_sts=None, region=None):
    table_name = module.params.get('name')
    hash_key_name = module.params.get('hash_key_name')
    hash_key_type = module.params.get('hash_key_type')
    range_key_name = module.params.get('range_key_name')
    range_key_type = module.params.get('range_key_type')
    read_capacity = module.params.get('read_capacity')
    write_capacity = module.params.get('write_capacity')
    all_indexes = module.params.get('indexes')
    tags = module.params.get('tags')
    wait_for_active_timeout = module.params.get('wait_for_active_timeout')
    for index in all_indexes:
        validate_index(index, module)
    schema = get_schema_param(hash_key_name, hash_key_type, range_key_name, range_key_type)
    throughput = {
        'read': read_capacity,
        'write': write_capacity,
    }
    (indexes, global_indexes) = get_indexes(all_indexes)
    result = dict(region=region, table_name=table_name, hash_key_name=hash_key_name, hash_key_type=hash_key_type, range_key_name=range_key_name, range_key_type=range_key_type, read_capacity=read_capacity, write_capacity=write_capacity, indexes=all_indexes)
    try:
        table = Table(table_name, connection=connection)
        if dynamo_table_exists(table):
            result['changed'] = update_dynamo_table(table, throughput=throughput, check_mode=module.check_mode, global_indexes=global_indexes)
        else:
            if (not module.check_mode):
                Table.create(table_name, connection=connection, schema=schema, throughput=throughput, indexes=indexes, global_indexes=global_indexes)
            result['changed'] = True
        if (not module.check_mode):
            result['table_status'] = table.describe()['Table']['TableStatus']
        if tags:
            wait_until_table_active(module, table, wait_for_active_timeout)
            account_id = get_account_id(boto3_sts)
            boto3_dynamodb.tag_resource(ResourceArn=((((('arn:aws:dynamodb:' + region) + ':') + account_id) + ':table/') + table_name), Tags=ansible_dict_to_boto3_tag_list(tags))
            result['tags'] = tags
    except BotoServerError:
        result['msg'] = ('Failed to create/update dynamo table due to error: ' + traceback.format_exc())
        module.fail_json(**result)
    else:
        module.exit_json(**result)
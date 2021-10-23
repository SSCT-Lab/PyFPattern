def create_resource(client, module, params, result):
    try:
        client.put_configuration_aggregator(ConfigurationAggregatorName=params['ConfigurationAggregatorName'], AccountAggregationSources=params['AccountAggregationSources'], OrganizationAggregationSource=params['OrganizationAggregationSource'])
        result['changed'] = True
        result['aggregator'] = camel_dict_to_snake_dict(resource_exists(client, module, params))
        return result
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg="Couldn't create AWS Config configuration aggregator")
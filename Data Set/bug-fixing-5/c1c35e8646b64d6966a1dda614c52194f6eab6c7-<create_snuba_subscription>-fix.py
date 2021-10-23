def create_snuba_subscription(project, dataset, query, aggregations, time_window, resolution):
    "\n    Creates a subscription to a snuba query.\n\n    :param project: The project we're applying the query to\n    :param dataset: The snuba dataset to query and aggregate over\n    :param query: An event search query that we can parse and convert into a\n    set of Snuba conditions\n    :param aggregations: A list of aggregations to calculate over the time\n    window\n    :param time_window: The time window to aggregate over\n    :param resolution: How often to receive updates/bucket size\n    :return: A uuid representing the subscription id.\n    "
    response = _snuba_pool.urlopen('POST', '/subscriptions', body=json.dumps({
        'project_id': project.id,
        'dataset': dataset.value,
        'conditions': get_snuba_query_args(query)['conditions'],
        'aggregates': [alert_aggregation_to_snuba[agg] for agg in aggregations],
        'time_window': time_window,
        'resolution': resolution,
    }), retries=False)
    if (response.status != 202):
        raise SnubaError(('HTTP %s response from Snuba!' % response.status))
    return uuid.UUID(json.loads(response.data)['subscription_id'])
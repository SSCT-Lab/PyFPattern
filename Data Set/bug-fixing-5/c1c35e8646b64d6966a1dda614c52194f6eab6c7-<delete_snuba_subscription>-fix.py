def delete_snuba_subscription(subscription_id):
    '\n    Deletes a subscription to a snuba query.\n    :param subscription_id: The uuid of the subscription to delete\n    :return:\n    '
    response = _snuba_pool.urlopen('DELETE', ('/subscriptions/%s' % subscription_id), retries=False)
    if (response.status != 202):
        raise SnubaError(('HTTP %s response from Snuba!' % response.status))
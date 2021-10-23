def delete_snuba_subscription(subscription_id):
    '\n    Deletes a subscription to a snuba query.\n    :param subscription_id: The uuid of the subscription to delete\n    :return:\n    '
    resp = safe_urlopen((settings.SENTRY_SNUBA + ('/subscriptions/%s' % subscription_id)), 'DELETE')
    resp.raise_for_status()
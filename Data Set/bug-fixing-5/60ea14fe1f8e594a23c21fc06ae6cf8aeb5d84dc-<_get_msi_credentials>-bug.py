def _get_msi_credentials(self, subscription_id_param=None):
    credentials = MSIAuthentication()
    try:
        subscription_client = SubscriptionClient(credentials)
        subscription = next(subscription_client.subscriptions.list())
        subscription_id = str(subscription.subscription_id)
        return {
            'credentials': credentials,
            'subscription_id': (subscription_id_param or subscription_id),
        }
    except Exception as exc:
        return None
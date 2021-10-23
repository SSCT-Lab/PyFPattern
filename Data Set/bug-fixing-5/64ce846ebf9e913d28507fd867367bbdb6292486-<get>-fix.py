def get(self, request, user):
    '\n        Retrieve Account Subscriptions\n        `````````````````````````````````````\n\n        Return list of subscriptions for an account\n\n        :auth: required\n        '
    sub = newsletter.get_subscriptions(user)
    if ((sub is None) or (not newsletter.is_enabled())):
        return Response([])
    try:
        return Response([{
            'listId': x.get('list_id'),
            'listDescription': x.get('list_description'),
            'listName': x.get('list_name'),
            'email': x.get('email'),
            'subscribed': x.get('subscribed'),
            'subscribedDate': x.get('subscribed_date'),
            'unsubscribedDate': x.get('unsubscribed_date'),
        } for x in sub['subscriptions']])
    except KeyError:
        return Response([])


def get(self, request, user):
    '\n        Retrieve Account Subscriptions\n        `````````````````````````````````````\n\n        Return list of subscriptions for an account\n\n        :auth: required\n        '
    sub = newsletter.get_subscriptions(user)
    if ((sub is None) or (not newsletter.is_enabled)):
        return Response([])
    try:
        return Response([{
            'listId': x['list_id'],
            'listDescription': x['list_description'],
            'listName': x['list_name'],
            'email': x['email'],
            'subscribed': x['subscribed'],
            'subscribedDate': x['subscribed_date'],
            'unsubscribedDate': x['unsubscribed_date'],
        } for x in sub['subscriptions']])
    except KeyError:
        return Response([])

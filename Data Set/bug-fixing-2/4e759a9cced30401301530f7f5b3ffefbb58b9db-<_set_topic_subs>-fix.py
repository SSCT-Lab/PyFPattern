

def _set_topic_subs(self):
    subscriptions_existing_list = []
    desired_subscriptions = [(sub['protocol'], self._canonicalize_endpoint(sub['protocol'], sub['endpoint'])) for sub in self.subscriptions]
    if self.subscriptions_existing:
        for sub in self.subscriptions_existing:
            sub_key = (sub['Protocol'], sub['Endpoint'])
            subscriptions_existing_list.append(sub_key)
            if (self.purge_subscriptions and (sub_key not in desired_subscriptions) and (sub['SubscriptionArn'] not in ('PendingConfirmation', 'Deleted'))):
                self.changed = True
                self.subscriptions_deleted.append(sub_key)
                if (not self.check_mode):
                    self.connection.unsubscribe(sub['SubscriptionArn'])
    for (protocol, endpoint) in desired_subscriptions:
        if ((protocol, endpoint) not in subscriptions_existing_list):
            self.changed = True
            self.subscriptions_added.append((protocol, endpoint))
            if (not self.check_mode):
                self.connection.subscribe(self.arn_topic, protocol, endpoint)

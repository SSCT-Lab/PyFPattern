def _delete_subscriptions(self):
    for sub in self.subscriptions_existing:
        if (sub['SubscriptionArn'] != 'PendingConfirmation'):
            self.subscriptions_deleted.append(sub['SubscriptionArn'])
            self.changed = True
            if (not self.check_mode):
                self.connection.unsubscribe(sub['SubscriptionArn'])
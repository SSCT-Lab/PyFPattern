def update_identity_notifications(connection, module):
    identity = module.params.get('identity')
    changed = False
    identity_notifications = get_identity_notifications(connection, module, identity)
    for notification_type in ('Bounce', 'Complaint', 'Delivery'):
        changed |= update_notification_topic(connection, module, identity, identity_notifications, notification_type)
        changed |= update_notification_topic_headers(connection, module, identity, identity_notifications, notification_type)
    changed |= update_feedback_forwarding(connection, module, identity, identity_notifications)
    if (changed or (identity_notifications is None)):
        identity_notifications = get_identity_notifications(connection, module, identity, retries=4)
    return (changed, identity_notifications)
def get_identity_notifications(connection, module, identity, retries=0, retryDelay=10):
    for attempt in range(0, (retries + 1)):
        response = call_and_handle_errors(module, connection.get_identity_notification_attributes, Identities=[identity])
        notification_attributes = response['NotificationAttributes']
        if (identity in notification_attributes):
            break
        elif (len(notification_attributes) != 0):
            module.fail_json(msg='Unexpected identity found in notification attributes, expected {0} but got {1!r}.'.format(identity, notification_attributes.keys()))
        time.sleep(retryDelay)
    if (identity not in notification_attributes):
        return None
    return notification_attributes[identity]
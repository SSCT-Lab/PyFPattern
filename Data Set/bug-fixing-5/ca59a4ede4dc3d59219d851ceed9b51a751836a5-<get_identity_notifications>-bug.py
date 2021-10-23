def get_identity_notifications(connection, module, identity):
    response = call_and_handle_errors(module, connection.get_identity_notification_attributes, Identities=[identity])
    notification_attributes = response['NotificationAttributes']
    if (identity not in notification_attributes):
        return None
    return notification_attributes[identity]
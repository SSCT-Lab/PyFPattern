def update_notification_topic(connection, module, identity, identity_notifications, notification_type):
    arg_dict = module.params.get((notification_type.lower() + '_notifications'))
    topic_key = (notification_type + 'Topic')
    if (topic_key in identity_notifications):
        current = identity_notifications[topic_key]
    else:
        current = None
    if ((arg_dict is not None) and ('topic' in arg_dict)):
        required = arg_dict['topic']
    else:
        required = None
    if (current != required):
        call_and_handle_errors(module, connection.set_identity_notification_topic, Identity=identity, NotificationType=notification_type, SnsTopic=required)
        return True
    return False
def update_feedback_forwarding(connection, module, identity, identity_notifications):
    if ('ForwardingEnabled' in identity_notifications):
        current = identity_notifications['ForwardingEnabled']
    else:
        current = False
    required = module.params.get('feedback_forwarding')
    if (current != required):
        call_and_handle_errors(module, connection.set_identity_feedback_forwarding_enabled, Identity=identity, ForwardingEnabled=required)
        return True
    return False
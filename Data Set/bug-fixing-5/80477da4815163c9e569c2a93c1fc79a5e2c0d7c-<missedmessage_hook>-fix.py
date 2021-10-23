def missedmessage_hook(user_profile_id: int, client: ClientDescriptor, last_for_client: bool) -> None:
    "The receiver_is_off_zulip logic used to determine whether a user\n    has no active client suffers from a somewhat fundamental race\n    condition.  If the client is no longer on the Internet,\n    receiver_is_off_zulip will still return true for\n    IDLE_EVENT_QUEUE_TIMEOUT_SECS, until the queue is\n    garbage-collected.  This would cause us to reliably miss\n    push/email notifying users for messages arriving during the\n    IDLE_EVENT_QUEUE_TIMEOUT_SECS after they suspend their laptop (for\n    example).  We address this by, when the queue is garbage-collected\n    at the end of those 10 minutes, checking to see if it's the last\n    one, and if so, potentially triggering notifications to the user\n    at that time, resulting in at most a IDLE_EVENT_QUEUE_TIMEOUT_SECS\n    delay in the arrival of their notifications.\n\n    As Zulip's APIs get more popular and the mobile apps start using\n    long-lived event queues for perf optimization, future versions of\n    this will likely need to replace checking `last_for_client` with\n    something more complicated, so that we only consider clients like\n    web browsers, not the mobile apps or random API scripts.\n    "
    if (not last_for_client):
        return
    for event in client.event_queue.contents():
        if (event['type'] != 'message'):
            continue
        assert ('flags' in event)
        flags = event.get('flags')
        if (flags is None):
            logging.error('Ignore missedmessage_hook for user {}.'.format(user_profile_id))
            return
        mentioned = (('mentioned' in flags) and ('read' not in flags))
        private_message = (event['message']['type'] == 'private')
        stream_push_notify = event.get('stream_push_notify', False)
        stream_name = None
        if (not private_message):
            stream_name = event['message']['display_recipient']
        always_push_notify = False
        idle = True
        message_id = event['message']['id']
        already_notified = dict(push_notified=event.get('push_notified', False), email_notified=event.get('email_notified', False))
        maybe_enqueue_notifications(user_profile_id, message_id, private_message, mentioned, stream_push_notify, stream_name, always_push_notify, idle, already_notified)
def _check_cross_realm_messages_archiving(self, arc_user_msg_qty: int, period: int, realm: Optional[Realm]=None) -> int:
    sent_message_id = self._send_cross_realm_message()
    all_user_messages_qty = UserMessage.objects.count()
    self._change_messages_pub_date([sent_message_id], (timezone_now() - timedelta(days=period)))
    realms = Realm.objects.filter(message_retention_days__isnull=False).order_by('id')
    for realm_instance in realms:
        move_expired_messages_to_archive(realm_instance)
        move_expired_user_messages_to_archive(realm_instance)
    user_messages_sent = UserMessage.objects.order_by('id').filter(message_id=sent_message_id)
    archived_messages = ArchivedMessage.objects.all()
    archived_user_messages = ArchivedUserMessage.objects.order_by('id')
    self.assertEqual(user_messages_sent.count(), 2)
    self.assertEqual(archived_messages.count(), 1)
    self.assertEqual(archived_user_messages.count(), arc_user_msg_qty)
    if realm:
        user_messages_sent = user_messages_sent.filter(user_profile__realm=self.zulip_realm)
    self.assertEqual([arc_user_msg.id for arc_user_msg in archived_user_messages], [user_msg.id for user_msg in user_messages_sent])
    for realm_instance in realms:
        delete_expired_user_messages(realm_instance)
        delete_expired_messages(realm_instance)
    clean_unused_messages()
    self.assertEqual(UserMessage.objects.filter(message_id=sent_message_id).count(), (2 - arc_user_msg_qty))
    self.assertEqual(UserMessage.objects.count(), (all_user_messages_qty - arc_user_msg_qty))
    return sent_message_id


def test_import_realm(self) -> None:
    original_realm = Realm.objects.get(string_id='zulip')
    RealmEmoji.objects.get(realm=original_realm).delete()
    huddle = [self.example_email('hamlet'), self.example_email('othello')]
    self.send_huddle_message(self.example_email('cordelia'), huddle, 'test huddle message')
    self._export_realm(original_realm)
    with patch('logging.info'):
        do_import_realm('var/test-export', 'test-zulip')
    self.assertTrue(Realm.objects.filter(string_id='test-zulip').exists())
    imported_realm = Realm.objects.get(string_id='test-zulip')
    self.assertNotEqual(imported_realm.id, original_realm.id)

    def assert_realm_values(f: Callable[([Realm], Any)], equal: bool=True) -> None:
        orig_realm_result = f(original_realm)
        imported_realm_result = f(imported_realm)
        if equal:
            self.assertEqual(orig_realm_result, imported_realm_result)
        else:
            self.assertNotEqual(orig_realm_result, imported_realm_result)
    assert_realm_values((lambda r: {user.email for user in r.get_admin_users()}))
    assert_realm_values((lambda r: {user.email for user in r.get_active_users()}))
    assert_realm_values((lambda r: {stream.name for stream in get_active_streams(r)}))

    def get_recipient_stream(r: Realm) -> Stream:
        return get_stream_recipient(Stream.objects.get(name='Verona', realm=r).id)

    def get_recipient_user(r: Realm) -> UserProfile:
        return get_personal_recipient(UserProfile.objects.get(full_name='Iago', realm=r).id)
    assert_realm_values((lambda r: get_recipient_stream(r).type))
    assert_realm_values((lambda r: get_recipient_user(r).type))

    def get_subscribers(recipient: Recipient) -> Set[str]:
        subscriptions = Subscription.objects.filter(recipient=recipient)
        users = {sub.user_profile.email for sub in subscriptions}
        return users
    assert_realm_values((lambda r: get_subscribers(get_recipient_stream(r))))
    assert_realm_values((lambda r: get_subscribers(get_recipient_user(r))))

    def get_custom_profile_field_names(r: Realm) -> Set[str]:
        custom_profile_fields = CustomProfileField.objects.filter(realm=r)
        custom_profile_field_names = {field.name for field in custom_profile_fields}
        return custom_profile_field_names
    assert_realm_values(get_custom_profile_field_names)

    def get_realm_audit_log_event_type(r: Realm) -> Set[str]:
        realmauditlogs = RealmAuditLog.objects.filter(realm=r)
        realmauditlog_event_type = {log.event_type for log in realmauditlogs}
        return realmauditlog_event_type
    assert_realm_values(get_realm_audit_log_event_type)

    def get_huddle_hashes(r: str) -> str:
        short_names = ['cordelia', 'hamlet', 'othello']
        user_id_list = [UserProfile.objects.get(realm=r, short_name=name).id for name in short_names]
        huddle_hash = get_huddle_hash(user_id_list)
        return huddle_hash
    assert_realm_values(get_huddle_hashes, equal=False)

    def get_huddle_message(r: str) -> str:
        huddle_hash = get_huddle_hashes(r)
        huddle_id = Huddle.objects.get(huddle_hash=huddle_hash).id
        huddle_recipient = Recipient.objects.get(type_id=huddle_id, type=3)
        huddle_message = Message.objects.get(recipient=huddle_recipient)
        return huddle_message.content
    assert_realm_values(get_huddle_message)
    self.assertEqual(get_huddle_message(imported_realm), 'test huddle message')

    def get_stream_messages(r: Realm) -> Message:
        recipient = get_recipient_stream(r)
        messages = Message.objects.filter(recipient=recipient)
        return messages

    def get_stream_topics(r: Realm) -> Set[str]:
        messages = get_stream_messages(r)
        topics = {m.subject for m in messages}
        return topics
    assert_realm_values(get_stream_topics)

    def get_usermessages_user(r: Realm) -> Set[Any]:
        messages = get_stream_messages(r).order_by('content')
        usermessage = UserMessage.objects.filter(message=messages[0])
        usermessage_user = {um.user_profile.email for um in usermessage}
        return usermessage_user
    assert_realm_values(get_usermessages_user)

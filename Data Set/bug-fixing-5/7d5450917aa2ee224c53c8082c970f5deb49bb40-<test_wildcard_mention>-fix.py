@mock.patch('zerver.lib.actions.send_event')
def test_wildcard_mention(self, mock_send_event: mock.MagicMock) -> None:
    stream_name = 'Macbeth'
    hamlet = self.example_user('hamlet')
    cordelia = self.example_user('cordelia')
    self.make_stream(stream_name, history_public_to_subscribers=True)
    self.subscribe(hamlet, stream_name)
    self.subscribe(cordelia, stream_name)
    self.login(hamlet.email)
    message_id = self.send_stream_message(hamlet.email, stream_name, 'Hello everyone')

    def notify(user_id: int) -> Dict[(str, Any)]:
        return {
            'id': user_id,
            'flags': ['wildcard_mentioned'],
        }
    users_to_be_notified = sorted(map(notify, [cordelia.id, hamlet.id]), key=itemgetter('id'))
    result = self.client_patch(('/json/messages/' + str(message_id)), {
        'message_id': message_id,
        'content': 'Hello @**everyone**',
    })
    self.assert_json_success(result)
    called = False
    for call_args in mock_send_event.call_args_list:
        (arg_realm, arg_event, arg_notified_users) = call_args[0]
        if (arg_event['type'] == 'update_message'):
            self.assertEqual(arg_event['type'], 'update_message')
            self.assertEqual(arg_event['wildcard_mention_user_ids'], [cordelia.id, hamlet.id])
            self.assertEqual(sorted(arg_notified_users, key=itemgetter('id')), users_to_be_notified)
            called = True
    self.assertTrue(called)
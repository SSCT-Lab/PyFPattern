

def test_send_message_errors(self):
    message = 'whatever'
    with self.simulated_markdown_failure():
        with self.assertRaisesRegexp(JsonableError, 'Unable to render message'):
            self.send_message('othello@zulip.com', 'Denmark', Recipient.STREAM, message)

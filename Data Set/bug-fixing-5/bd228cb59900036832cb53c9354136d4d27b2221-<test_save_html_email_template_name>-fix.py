def test_save_html_email_template_name(self):
    '\n        Test the PasswordResetForm.save() method with html_email_template_name\n        parameter specified.\n        Test to ensure that a multipart email is sent with both text/plain\n        and text/html parts.\n        '
    (user, username, email) = self.create_dummy_user()
    form = PasswordResetForm({
        'email': email,
    })
    self.assertTrue(form.is_valid())
    form.save(html_email_template_name='registration/html_password_reset_email.html')
    self.assertEqual(len(mail.outbox), 1)
    self.assertEqual(len(mail.outbox[0].alternatives), 1)
    message = mail.outbox[0].message()
    self.assertEqual(message.get('subject'), 'Custom password reset on example.com')
    self.assertEqual(len(message.get_payload()), 2)
    self.assertTrue(message.is_multipart())
    self.assertEqual(message.get_payload(0).get_content_type(), 'text/plain')
    self.assertEqual(message.get_payload(1).get_content_type(), 'text/html')
    self.assertEqual(message.get_all('to'), [email])
    self.assertTrue(re.match('^http://example.com/reset/[\\w/-]+', message.get_payload(0).get_payload()))
    self.assertTrue(re.match('^<html><a href="http://example.com/reset/[\\w/-]+/">Link</a></html>$', message.get_payload(1).get_payload()))
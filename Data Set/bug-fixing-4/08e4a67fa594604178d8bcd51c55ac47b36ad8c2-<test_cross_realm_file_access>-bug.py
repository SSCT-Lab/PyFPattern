def test_cross_realm_file_access(self):

    def create_user(email):
        self.register(email, 'test')
        return get_user_profile_by_email(email)
    user1_email = 'user1@uploadtest.example.com'
    user2_email = 'test-og-bot@zulip.com'
    user3_email = 'other-user@uploadtest.example.com'
    settings.CROSS_REALM_BOT_EMAILS.add(user2_email)
    settings.CROSS_REALM_BOT_EMAILS.add(user3_email)
    dep = Deployment()
    dep.base_api_url = 'https://zulip.com/api/'
    dep.base_site_url = 'https://zulip.com/'
    dep.save()
    dep.realms = [get_realm('zulip')]
    dep.save()
    r1 = Realm.objects.create(string_id='uploadtest.example.com', invite_required=False)
    RealmDomain.objects.create(realm=r1, domain='uploadtest.example.com')
    deployment = Deployment.objects.filter()[0]
    deployment.realms.add(r1)
    create_user(user1_email)
    create_user(user2_email)
    create_user(user3_email)
    self.login(user2_email, 'test')
    fp = StringIO('zulip!')
    fp.name = 'zulip.txt'
    result = self.client_post('/json/upload_file', {
        'file': fp,
    })
    json = ujson.loads(result.content)
    uri = json['uri']
    fp_path_id = re.sub('/user_uploads/', '', uri)
    body = (('First message ...[zulip.txt](http://localhost:9991/user_uploads/' + fp_path_id) + ')')
    self.send_message(user2_email, user1_email, Recipient.PERSONAL, body)
    self.login(user1_email, 'test')
    response = self.client_get(uri)
    self.assertEqual(response.status_code, 200)
    data = b''.join(response.streaming_content)
    self.assertEqual(b'zulip!', data)
    self.client_post('/accounts/logout/')
    self.login(user3_email, 'test')
    response = self.client_get(uri)
    self.assertEqual(response.status_code, 403)
    self.assert_in_response('You are not authorized to view this file.', response)
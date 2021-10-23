def test_basic_resolving(self):
    url = reverse('sentry-api-0-dsym-files', kwargs={
        'organization_slug': self.project.organization.slug,
        'project_slug': self.project.slug,
    })
    self.login_as(user=self.user)
    out = BytesIO()
    f = zipfile.ZipFile(out, 'w')
    f.writestr(('proguard/%s.txt' % PROGUARD_UUID), PROGUARD_SOURCE)
    f.writestr('ignored-file.txt', b'This is just some stuff')
    f.close()
    response = self.client.post(url, {
        'file': SimpleUploadedFile('symbols.zip', out.getvalue(), content_type='application/zip'),
    }, format='multipart')
    assert (response.status_code == 201), response.content
    assert (len(response.data) == 1)
    event_data = {
        'user': {
            'ip_address': '31.172.207.97',
        },
        'extra': {
            
        },
        'project': self.project.id,
        'platform': 'java',
        'debug_meta': {
            'images': [{
                'type': 'proguard',
                'uuid': PROGUARD_UUID,
            }],
        },
        'exception': {
            'values': [{
                'stacktrace': {
                    'frames': [{
                        'function': 'a',
                        'abs_path': None,
                        'module': 'org.a.b.g$a',
                        'filename': None,
                        'lineno': 67,
                    }, {
                        'function': 'a',
                        'abs_path': None,
                        'module': 'org.a.b.g$a',
                        'filename': None,
                        'lineno': 69,
                    }],
                },
                'type': 'RuntimeException',
                'value': 'Shit broke yo',
            }],
        },
    }
    resp = self._postWithHeader(event_data)
    with self.assertWriteQueries({
        'nodestore_node': 2,
        'sentry_eventuser': 1,
        'sentry_groupedmessage': 1,
        'sentry_message': 1,
        'sentry_userip': 1,
        'sentry_userreport': 1,
    }):
        self._postWithHeader(event_data)
    assert (resp.status_code == 200)
    event_id = json.loads(resp.content)['id']
    event = eventstore.get_event_by_id(self.project.id, event_id)
    bt = event.interfaces['exception'].values[0].stacktrace
    frames = bt.frames
    assert (frames[0].function == 'getClassContext')
    assert (frames[0].module == 'org.slf4j.helpers.Util$ClassContextSecurityManager')
    assert (frames[1].function == 'getExtraClassContext')
    assert (frames[1].module == 'org.slf4j.helpers.Util$ClassContextSecurityManager')
    assert (event.culprit == 'org.slf4j.helpers.Util$ClassContextSecurityManager in getExtraClassContext')
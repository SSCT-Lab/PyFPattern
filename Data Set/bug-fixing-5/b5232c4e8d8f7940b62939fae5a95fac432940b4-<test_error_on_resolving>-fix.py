def test_error_on_resolving(self):
    url = reverse('sentry-api-0-dsym-files', kwargs={
        'organization_slug': self.project.organization.slug,
        'project_slug': self.project.slug,
    })
    self.login_as(user=self.user)
    out = BytesIO()
    f = zipfile.ZipFile(out, 'w')
    f.writestr(('proguard/%s.txt' % PROGUARD_BUG_UUID), PROGUARD_BUG_SOURCE)
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
                'uuid': PROGUARD_BUG_UUID,
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
        'timestamp': iso_format(before_now(seconds=1)),
    }
    resp = self._postWithHeader(event_data)
    assert (resp.status_code == 200)
    event_id = json.loads(resp.content)['id']
    event = eventstore.get_event_by_id(self.project.id, event_id)
    assert (len(event.data['errors']) == 1)
    assert (event.data['errors'][0] == {
        'mapping_uuid': '071207ac-b491-4a74-957c-2c94fd9594f2',
        'type': 'proguard_missing_lineno',
    })
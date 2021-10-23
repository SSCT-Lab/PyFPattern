def test_debug_id_resolving(self):
    file = File.objects.create(name='crash.pdb', type='default', headers={
        'Content-Type': 'text/x-breakpad',
    })
    path = get_fixture_path('windows.sym')
    with open(path) as f:
        file.putfile(f)
    ProjectDebugFile.objects.create(file=file, object_name='crash.pdb', cpu_name='x86', project=self.project, debug_id='3249d99d-0c40-4931-8610-f4e4fb0b6936-1', code_id='5AB380779000')
    self.login_as(user=self.user)
    event_data = {
        'contexts': {
            'device': {
                'arch': 'x86',
            },
            'os': {
                'build': '',
                'name': 'Windows',
                'type': 'os',
                'version': '10.0.14393',
            },
        },
        'debug_meta': {
            'images': [{
                'id': '3249d99d-0c40-4931-8610-f4e4fb0b6936-1',
                'image_addr': '0x2a0000',
                'image_size': 36864,
                'name': 'C:\\projects\\breakpad-tools\\windows\\Release\\crash.exe',
                'type': 'symbolic',
            }],
        },
        'exception': {
            'stacktrace': {
                'frames': [{
                    'function': '<unknown>',
                    'instruction_addr': '0x2a2a3d',
                    'package': 'C:\\projects\\breakpad-tools\\windows\\Release\\crash.exe',
                }],
            },
            'thread_id': 1636,
            'type': 'EXCEPTION_ACCESS_VIOLATION_WRITE',
            'value': 'Fatal Error: EXCEPTION_ACCESS_VIOLATION_WRITE',
        },
        'platform': 'native',
    }
    resp = self._postWithHeader(event_data)
    assert (resp.status_code == 200)
    event = self.get_event()
    assert (event.data['culprit'] == 'main')
    insta_snapshot_stacktrace_data(self, event.data)
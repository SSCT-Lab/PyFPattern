def assertReportCreated(self, input, output):
    resp = self._postCspWithHeader(input)
    assert (resp.status_code == 201), resp.content
    events = eventstore.get_events(filter_keys={
        'project_id': [self.project.id],
    }, conditions=[['type', '=', 'csp']])
    assert (len(events) == 1)
    e = events[0]
    Event.objects.bind_nodes([e], 'data')
    assert (output['message'] == e.data['logentry']['formatted'])
    for (key, value) in six.iteritems(output['tags']):
        assert (e.get_tag(key) == value)
    for (key, value) in six.iteritems(output['data']):
        assert (e.data[key] == value)
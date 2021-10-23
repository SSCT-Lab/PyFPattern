

def test_unmerge(self):
    now = datetime(2017, 5, 3, 6, 6, 6, tzinfo=pytz.utc)

    def shift(i):
        return timedelta(seconds=(1 << i))
    project = self.create_project()
    source = self.create_group(project)
    sequence = itertools.count(0)
    tag_values = itertools.cycle(['red', 'green', 'blue'])
    user_values = itertools.cycle([{
        'id': 1,
    }, {
        'id': 2,
    }])
    EnvironmentProject.objects.create(environment=Environment.objects.create(organization_id=project.organization_id, name='production'), project=project)

    def create_message_event(template, parameters):
        i = next(sequence)
        event_id = uuid.UUID(fields=(i, 0, 4096, 128, 128, 141289400074368)).hex
        event = Event.objects.create(project_id=project.id, group_id=source.id, event_id=event_id, message=('%s' % (id,)), datetime=(now + shift(i)), data={
            'environment': 'production',
            'type': 'default',
            'metadata': {
                'title': (template % parameters),
            },
            'sentry.interfaces.Message': {
                'message': template,
                'params': parameters,
                'formatted': (template % parameters),
            },
            'sentry.interfaces.User': next(user_values),
            'tags': [['color', next(tag_values)], ['environment', 'production'], ['sentry:release', 'version']],
        })
        with self.tasks():
            Group.objects.add_tags(source, tags=event.get_tags())
        EventMapping.objects.create(project_id=project.id, group_id=source.id, event_id=event_id, date_added=event.datetime)
        UserReport.objects.create(project_id=project.id, group_id=source.id, event_id=event_id, name='Log Hat', email='ceo@corptron.com', comments='Quack')
        features.record(event)
        return event
    events = OrderedDict()
    for event in (create_message_event('This is message #%s.', i) for i in xrange(10)):
        events.setdefault(get_fingerprint(event), []).append(event)
    for event in (create_message_event('This is message #%s!', i) for i in xrange(10, 17)):
        events.setdefault(get_fingerprint(event), []).append(event)
    assert (len(events) == 2)
    assert (sum(map(len, events.values())) == 17)
    for fingerprint in events.keys():
        GroupHash.objects.create(project=project, group=source, hash=fingerprint)
    assert (set(GroupTagKey.objects.filter(group=source).values_list('key', 'values_seen')) == set([('color', 3), ('environment', 1), ('sentry:release', 1)]))
    assert (set(GroupTagValue.objects.filter(group_id=source.id).values_list('key', 'value', 'times_seen')) == set([('color', 'red', 6), ('color', 'green', 6), ('color', 'blue', 5), ('environment', 'production', 17), ('sentry:release', 'version', 17)]))
    assert (features.query(source) == [(source.id, {
        'message:message:character-shingles': 1.0,
    })])
    with self.tasks():
        unmerge.delay(source.project_id, source.id, None, [events.keys()[1]], None, batch_size=5)
    assert (list(Group.objects.filter(id=source.id).values_list('times_seen', 'first_seen', 'last_seen')) == [(10, (now + shift(0)), (now + shift(9)))])
    source_activity = Activity.objects.get(group_id=source.id, type=Activity.UNMERGE_SOURCE)
    destination = Group.objects.get(id=source_activity.data['destination_id'])
    assert (list(Group.objects.filter(id=destination.id).values_list('times_seen', 'first_seen', 'last_seen')) == [(7, (now + shift(10)), (now + shift(16)))])
    assert (source_activity.data == {
        'destination_id': destination.id,
        'fingerprints': [events.keys()[1]],
    })
    assert (source.id != destination.id)
    assert (source.project == destination.project)
    assert (Activity.objects.get(group_id=destination.id, type=Activity.UNMERGE_DESTINATION).data == {
        'source_id': source.id,
        'fingerprints': [events.keys()[1]],
    })
    source_event_event_ids = map((lambda event: event.event_id), events.values()[0])
    assert (source.event_set.count() == 10)
    assert (set(EventMapping.objects.filter(group_id=source.id).values_list('event_id', flat=True)) == set(source_event_event_ids))
    assert (set(UserReport.objects.filter(group_id=source.id).values_list('event_id', flat=True)) == set(source_event_event_ids))
    assert (set(GroupHash.objects.filter(group_id=source.id).values_list('hash', flat=True)) == set([events.keys()[0]]))
    assert (set(GroupRelease.objects.filter(group_id=source.id).values_list('environment', 'first_seen', 'last_seen')) == set([('production', (now + shift(0)), (now + shift(9)))]))
    assert (set(GroupTagKey.objects.filter(group=source).values_list('key', 'values_seen')) == set([('color', 3), ('environment', 1), ('sentry:release', 1)]))
    assert (set(GroupTagValue.objects.filter(group_id=source.id).values_list('key', 'value', 'times_seen', 'first_seen', 'last_seen')) == set([('color', 'red', 4, (now + shift(0)), (now + shift(9))), ('color', 'green', 3, (now + shift(1)), (now + shift(7))), ('color', 'blue', 3, (now + shift(2)), (now + shift(8))), ('environment', 'production', 10, (now + shift(0)), (now + shift(9))), ('sentry:release', 'version', 10, (now + shift(0)), (now + shift(9)))]))
    destination_event_event_ids = map((lambda event: event.event_id), events.values()[1])
    assert (destination.event_set.count() == 7)
    assert (set(EventMapping.objects.filter(group_id=destination.id).values_list('event_id', flat=True)) == set(destination_event_event_ids))
    assert (set(UserReport.objects.filter(group_id=destination.id).values_list('event_id', flat=True)) == set(destination_event_event_ids))
    assert (set(GroupHash.objects.filter(group_id=destination.id).values_list('hash', flat=True)) == set([events.keys()[1]]))
    assert (set(GroupRelease.objects.filter(group_id=destination.id).values_list('environment', 'first_seen', 'last_seen')) == set([('production', (now + shift(10)), (now + shift(16)))]))
    assert (set(GroupTagKey.objects.filter(group=destination).values_list('key', 'values_seen')) == set([('color', 3), ('environment', 1), ('sentry:release', 1)]))
    assert (set(GroupTagValue.objects.filter(group_id=destination.id).values_list('key', 'value', 'times_seen', 'first_seen', 'last_seen')) == set([('color', 'red', 2, (now + shift(12)), (now + shift(15))), ('color', 'green', 3, (now + shift(10)), (now + shift(16))), ('color', 'blue', 2, (now + shift(11)), (now + shift(14))), ('environment', 'production', 7, (now + shift(10)), (now + shift(16))), ('sentry:release', 'version', 7, (now + shift(10)), (now + shift(16)))]))
    time_series = tsdb.get_range(tsdb.models.group, [source.id, destination.id], now, (now + shift(16)))

    def get_expected_series_values(rollup, events, function=None):
        if (function is None):

            def function(aggregate, event):
                return ((aggregate if (aggregate is not None) else 0) + 1)
        expected = {
            
        }
        for event in events:
            k = float(((to_timestamp(event.datetime) // rollup_duration) * rollup_duration))
            expected[k] = function(expected.get(k), event)
        return expected

    def assert_series_contains(expected, actual, default=0):
        actual = dict(actual)
        for (key, value) in expected.items():
            assert (actual[key] == value)
        for key in (set(actual.keys()) - set(expected.keys())):
            assert (actual[key] == default)
    rollup_duration = (time_series.values()[0][1][0] - time_series.values()[0][0][0])
    assert_series_contains(get_expected_series_values(rollup_duration, events.values()[0]), time_series[source.id], 0)
    assert_series_contains(get_expected_series_values(rollup_duration, events.values()[1]), time_series[destination.id], 0)
    time_series = tsdb.get_distinct_counts_series(tsdb.models.users_affected_by_group, [source.id, destination.id], now, (now + shift(16)))
    rollup_duration = (time_series.values()[0][1][0] - time_series.values()[0][0][0])

    def collect_by_user_tag(aggregate, event):
        aggregate = (aggregate if (aggregate is not None) else set())
        aggregate.add(get_event_user_from_interface(event.data['sentry.interfaces.User']).tag_value)
        return aggregate
    assert_series_contains({timestamp: len(values) for (timestamp, values) in get_expected_series_values(rollup_duration, events.values()[0], collect_by_user_tag).items()}, time_series[source.id])
    assert_series_contains({timestamp: len(values) for (timestamp, values) in get_expected_series_values(rollup_duration, events.values()[1], collect_by_user_tag).items()}, time_series[destination.id])
    time_series = tsdb.get_most_frequent_series(tsdb.models.frequent_releases_by_group, [source.id, destination.id], now, (now + shift(16)))
    rollup_duration = (time_series.values()[0][1][0] - time_series.values()[0][0][0])

    def collect_by_release(group, aggregate, event):
        aggregate = (aggregate if (aggregate is not None) else {
            
        })
        release = GroupRelease.objects.get(group_id=group.id, environment=event.data['environment'], release_id=Release.objects.get(organization_id=project.organization_id, version=event.get_tag('sentry:release')).id).id
        aggregate[release] = (aggregate.get(release, 0) + 1)
        return aggregate
    assert_series_contains(get_expected_series_values(rollup_duration, events.values()[0], functools.partial(collect_by_release, source)), time_series[source.id], {
        
    })
    assert_series_contains(get_expected_series_values(rollup_duration, events.values()[1], functools.partial(collect_by_release, destination)), time_series[destination.id], {
        
    })
    time_series = tsdb.get_most_frequent_series(tsdb.models.frequent_environments_by_group, [source.id, destination.id], now, (now + shift(16)))
    rollup_duration = (time_series.values()[0][1][0] - time_series.values()[0][0][0])

    def collect_by_environment(aggregate, event):
        aggregate = (aggregate if (aggregate is not None) else {
            
        })
        environment = Environment.objects.get(organization_id=project.organization_id, name=event.data['environment']).id
        aggregate[environment] = (aggregate.get(environment, 0) + 1)
        return aggregate
    assert_series_contains(get_expected_series_values(rollup_duration, events.values()[0], collect_by_environment), time_series[source.id], {
        
    })
    assert_series_contains(get_expected_series_values(rollup_duration, events.values()[1], collect_by_environment), time_series[destination.id], {
        
    })
    source_similar_items = features.query(source)
    assert (source_similar_items[0] == (source.id, {
        'message:message:character-shingles': 1.0,
    }))
    assert (source_similar_items[1][0] == destination.id)
    assert (source_similar_items[1][1].keys() == ['message:message:character-shingles'])
    assert (source_similar_items[1][1]['message:message:character-shingles'] < 1.0)
    destination_similar_items = features.query(destination)
    assert (destination_similar_items[0] == (destination.id, {
        'message:message:character-shingles': 1.0,
    }))
    assert (destination_similar_items[1][0] == source.id)
    assert (destination_similar_items[1][1].keys() == ['message:message:character-shingles'])
    assert (destination_similar_items[1][1]['message:message:character-shingles'] < 1.0)

def test_updates_group(self):
    manager = EventManager(make_event(message='foo', event_id=('a' * 32), checksum=('a' * 32)))
    manager.normalize()
    event = manager.save(1)
    manager = EventManager(make_event(message='foo bar', event_id=('b' * 32), checksum=('a' * 32)))
    manager.normalize()
    with self.tasks():
        event2 = manager.save(1)
    group = Group.objects.get(id=event.group_id)
    assert (group.times_seen == 2)
    assert (group.last_seen.replace(microsecond=0) == event.datetime.replace(microsecond=0))
    assert (group.message == event2.message)
    assert (group.data.get('type') == 'default')
    assert (group.data.get('metadata') == {
        'title': 'foo bar',
    })
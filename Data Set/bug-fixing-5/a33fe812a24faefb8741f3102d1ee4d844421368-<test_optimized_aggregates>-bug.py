@mock.patch('sentry.utils.snuba.query')
def test_optimized_aggregates(self, query_mock):
    query_mock.return_value = {
        
    }

    def Any(cls):

        class Any(object):

            def __eq__(self, other):
                return isinstance(other, cls)
        return Any()
    common_args = {
        'start': Any(datetime),
        'end': Any(datetime),
        'filter_keys': {
            'project_id': [self.project.id],
            'primary_hash': ['513772ee53011ad9f4dc374b2d34d0e9'],
        },
        'groupby': ['primary_hash'],
        'conditions': [],
        'limit': Any(int),
    }
    self.backend.query(self.project, query='foo')
    assert (query_mock.call_args == mock.call(orderby='-last_seen', aggregations=[['max', 'timestamp', 'last_seen']], having=[], **common_args))
    self.backend.query(self.project, query='foo', sort_by='date', last_seen_from=timezone.now())
    assert (query_mock.call_args == mock.call(orderby='-last_seen', aggregations=[['max', 'timestamp', 'last_seen']], having=[('last_seen', '>=', Any(int))], **common_args))
    self.backend.query(self.project, query='foo', sort_by='priority')
    assert (query_mock.call_args == mock.call(orderby='-priority', aggregations=[['toUInt32(log(times_seen) * 600) + toUInt32(last_seen)', '', 'priority'], ['count()', '', 'times_seen'], ['max', 'timestamp', 'last_seen']], having=[], **common_args))
    self.backend.query(self.project, query='foo', sort_by='freq', times_seen=5)
    assert (query_mock.call_args == mock.call(orderby='-times_seen', aggregations=[['count()', '', 'times_seen']], having=[('times_seen', '=', 5)], **common_args))
    self.backend.query(self.project, query='foo', sort_by='new', age_from=timezone.now())
    assert (query_mock.call_args == mock.call(orderby='-first_seen', aggregations=[['min', 'timestamp', 'first_seen']], having=[('first_seen', '>=', Any(int))], **common_args))
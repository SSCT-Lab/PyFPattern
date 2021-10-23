def generate_transaction():
    event_data = load_data('transaction')
    start_datetime = before_now(minutes=1)
    end_datetime = (start_datetime + timedelta(milliseconds=500))

    def generate_timestamp(date_time):
        return (time.mktime(date_time.utctimetuple()) + (date_time.microsecond / 1000000.0))
    event_data['start_timestamp'] = generate_timestamp(start_datetime)
    event_data['timestamp'] = generate_timestamp(end_datetime)
    reference_span = event_data['spans'][0]
    parent_span_id = reference_span['parent_span_id']
    span_tree_blueprint = {
        'a': {
            'aa': {
                'aaa': {
                    'aaaa': 'aaaaa',
                },
            },
        },
        'b': {
            
        },
        'c': {
            
        },
        'd': {
            
        },
        'e': {
            
        },
    }
    time_offsets = {
        'a': (timedelta(), timedelta(milliseconds=250)),
        'aa': (timedelta(milliseconds=10), timedelta(milliseconds=20)),
        'aaa': (timedelta(milliseconds=15), timedelta(milliseconds=30)),
        'aaaa': (timedelta(milliseconds=20), timedelta(milliseconds=50)),
        'aaaaa': (timedelta(milliseconds=25), timedelta(milliseconds=50)),
        'b': (timedelta(milliseconds=100), timedelta(milliseconds=100)),
        'c': (timedelta(milliseconds=350), timedelta(milliseconds=50)),
        'd': (timedelta(milliseconds=375), timedelta(milliseconds=50)),
        'e': (timedelta(milliseconds=400), timedelta(milliseconds=100)),
    }

    def build_span_tree(span_tree, spans, parent_span_id):
        for (span_id, child) in span_tree.items():
            span = copy.deepcopy(reference_span)
            span['parent_span_id'] = parent_span_id.ljust(16, '0')
            span['span_id'] = span_id.ljust(16, '0')
            (start_delta, span_length) = time_offsets.get(span_id, (timedelta(), timedelta()))
            span_start_time = (start_datetime + start_delta)
            span['start_timestamp'] = generate_timestamp(span_start_time)
            span['timestamp'] = generate_timestamp((span_start_time + span_length))
            spans.append(span)
            if isinstance(child, dict):
                spans = build_span_tree(child, spans, span_id)
            elif isinstance(child, six.string_types):
                parent_span_id = span_id
                span_id = child
                span = copy.deepcopy(reference_span)
                span['parent_span_id'] = parent_span_id.ljust(16, '0')
                span['span_id'] = span_id.ljust(16, '0')
                (start_delta, span_length) = time_offsets.get(span_id, (timedelta(), timedelta()))
                span_start_time = (start_datetime + start_delta)
                span['start_timestamp'] = generate_timestamp(span_start_time)
                span['timestamp'] = generate_timestamp((span_start_time + span_length))
                spans.append(span)
        return spans
    event_data['spans'] = build_span_tree(span_tree_blueprint, [], parent_span_id)
    return event_data
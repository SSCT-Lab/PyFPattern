def normalize(self):
    tags = {
        'use_rust_normalize': six.text_type(self.use_rust_normalize),
    }
    with metrics.timer('events.store.normalize.duration', tags=tags):
        self._normalize_impl()
    data = self.get_data()
    data['use_rust_normalize'] = self.use_rust_normalize
    metrics.timing('events.store.normalize.errors', len((data.get('errors') or ())), tags=tags)
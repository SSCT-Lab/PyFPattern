

def normalize(self):
    tags = {
        'project_id': six.text_type((self._project.id if (self._project and self.use_rust_normalize) else None)),
        'use_rust_normalize': six.text_type(self.use_rust_normalize),
    }
    with metrics.timer('events.store.normalize.duration', tags=tags):
        self._normalize_impl()
    data = self.get_data()
    data['use_rust_normalize'] = self.use_rust_normalize
    metrics.timing('events.store.normalize.errors', len((data.get('errors') or ())), tags=tags)

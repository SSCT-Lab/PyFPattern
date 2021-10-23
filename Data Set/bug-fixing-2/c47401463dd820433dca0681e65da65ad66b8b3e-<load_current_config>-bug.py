

def load_current_config(self):
    self._current_config = dict()
    lag_types = set([lag_obj['type'] for lag_obj in self._required_config])
    for lag_type in lag_types:
        if_type = self.IF_TYPE_MAP[lag_type]
        lag_summary = self._get_port_channels(if_type)
        if lag_summary:
            self._parse_port_channels_summary(lag_type, lag_summary)
    with open('/tmp/linagg.txt', 'w') as fp:
        fp.write(('current_config: %s\n' % self._current_config))
        fp.write(('required_config: %s\n' % self._required_config))

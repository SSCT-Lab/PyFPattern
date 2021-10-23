def _construct_parameters(self, **kwargs):
    'Contruct parameters.\n\n        Args:\n            **kwargs: Arbitrary keyword parameters.\n\n        Returns:\n            dict: dictionary of specified parameters\n        '
    _params = {
        'name': kwargs['name'],
        'eventsource': to_numeric_value(['trigger', 'discovery', 'auto_registration', 'internal'], kwargs['event_source']),
        'esc_period': kwargs.get('esc_period'),
        'filter': kwargs['conditions'],
        'def_longdata': kwargs['default_message'],
        'def_shortdata': kwargs['default_subject'],
        'r_longdata': kwargs['recovery_default_message'],
        'r_shortdata': kwargs['recovery_default_subject'],
        'ack_longdata': kwargs['acknowledge_default_message'],
        'ack_shortdata': kwargs['acknowledge_default_subject'],
        'operations': kwargs['operations'],
        'recovery_operations': kwargs.get('recovery_operations'),
        'acknowledge_operations': kwargs.get('acknowledge_operations'),
        'status': to_numeric_value(['enabled', 'disabled'], kwargs['status']),
    }
    if (float(self._zapi.api_version().rsplit('.', 1)[0]) >= 4.0):
        _params['pause_suppressed'] = ('1' if kwargs['pause_in_maintenance'] else '0')
    else:
        _params['maintenance_mode'] = ('1' if kwargs['pause_in_maintenance'] else '0')
    return _params
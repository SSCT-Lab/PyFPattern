

def _construct_opconditions(self, operation):
    'Construct operation conditions.\n\n        Args:\n            operation: operation to construct the conditions\n\n        Returns:\n            list: constructed operation conditions\n        '
    _opcond = operation.get('operation_condition')
    if (_opcond is not None):
        if (_opcond == 'acknowledged'):
            _value = '1'
        elif (_opcond == 'not_acknowledged'):
            _value = '0'
        return [{
            'conditiontype': '14',
            'operator': '0',
            'value': _value,
        }]
    return []

def _check_data_type_forward(self, in_data):
    in_type = type_check.get_types(in_data, 'in_types', False)
    try:
        self.check_type_forward(in_type)
    except type_check.InvalidType as e:
        msg = '\nInvalid operation is performed in: {0} (Forward)\n\n{1}'.format(self.label, str(e))
        raise type_check.InvalidType(e.expect, e.actual, msg=msg)
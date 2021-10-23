def boolean(self, arg):
    ' return a bool for the arg '
    if ((arg is None) or isinstance(arg, bool)):
        return arg
    if isinstance(arg, string_types):
        arg = arg.lower()
    if (arg in BOOLEANS_TRUE):
        return True
    elif (arg in BOOLEANS_FALSE):
        return False
    else:
        self.fail_json(msg=('%s is not a valid boolean. Valid booleans include: %s' % (to_text(arg), ','.join([('%s' % x) for x in BOOLEANS]))))
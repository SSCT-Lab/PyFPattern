

def parse_kv_args(self, args):
    'parse key-value style arguments'
    for arg in ['start', 'end', 'count', 'stride']:
        try:
            arg_raw = args.pop(arg, None)
            if (arg_raw is None):
                continue
            arg_cooked = int(arg_raw, 0)
            setattr(self, arg, arg_cooked)
        except ValueError:
            raise AnsibleError(("can't parse arg %s=%r as integer" % (arg, arg_raw)))
    if ('format' in args):
        self.format = args.pop('format')
    if args:
        raise AnsibleError(('unrecognized arguments to with_sequence: %r' % args.keys()))

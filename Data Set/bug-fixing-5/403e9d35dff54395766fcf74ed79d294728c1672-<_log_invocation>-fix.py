def _log_invocation(self):
    ' log that ansible ran the module '
    log_args = dict()
    for param in self.params:
        canon = self.aliases.get(param, param)
        arg_opts = self.argument_spec.get(canon, {
            
        })
        no_log = arg_opts.get('no_log', False)
        arg_type = arg_opts.get('type', 'str')
        if self.boolean(no_log):
            log_args[param] = 'NOT_LOGGING_PARAMETER'
        elif ((arg_type != 'bool') and PASSWORD_MATCH.search(param)):
            log_args[param] = 'NOT_LOGGING_PASSWORD'
            self.warn(('Module did not set no_log for %s' % param))
        else:
            param_val = self.params[param]
            if (not isinstance(param_val, (text_type, binary_type))):
                param_val = str(param_val)
            elif isinstance(param_val, text_type):
                param_val = param_val.encode('utf-8')
            log_args[param] = heuristic_log_sanitize(param_val, self.no_log_values)
    msg = []
    for arg in log_args:
        arg_val = log_args[arg]
        if (not isinstance(arg_val, (text_type, binary_type))):
            arg_val = str(arg_val)
        elif isinstance(arg_val, text_type):
            arg_val = arg_val.encode('utf-8')
        msg.append(('%s=%s' % (arg, arg_val)))
    if msg:
        msg = ('Invoked with %s' % ' '.join(msg))
    else:
        msg = 'Invoked'
    self.log(msg, log_args=log_args)
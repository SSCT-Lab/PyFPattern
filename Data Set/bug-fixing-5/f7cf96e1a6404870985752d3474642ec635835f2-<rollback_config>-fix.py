def rollback_config(module, result):
    rollback = module.params['rollback']
    kwargs = dict(comment=module.params['comment'], commit=(not module.check_mode))
    diff = module.connection.rollback_config(rollback, **kwargs)
    if diff:
        result['changed'] = True
        result['diff'] = dict(prepared=diff)
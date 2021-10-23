def _post_monitor(module, options):
    try:
        kwargs = dict(type=module.params['type'], query=module.params['query'], name=module.params['name'], message=_fix_template_vars(module.params['message']), options=options)
        if (module.params['tags'] is not None):
            kwargs['tags'] = module.params['tags']
        msg = api.Monitor.create(**kwargs)
        if ('errors' in msg):
            module.fail_json(msg=str(msg['errors']))
        else:
            module.exit_json(changed=True, msg=msg)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())
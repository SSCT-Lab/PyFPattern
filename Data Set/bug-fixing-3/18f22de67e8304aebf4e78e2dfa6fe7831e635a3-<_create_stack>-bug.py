def _create_stack(module, stack, cloud, sdk):
    try:
        stack = cloud.create_stack(module.params['name'], tags=module.params['tag'], template_file=module.params['template'], environment_files=module.params['environment'], timeout=module.params['timeout'], wait=True, rollback=module.params['rollback'], **module.params['parameters'])
        stack = cloud.get_stack(stack.id, None)
        if (stack.stack_status == 'CREATE_COMPLETE'):
            return stack
        else:
            module.fail_json(msg='Failure in creating stack: {0}'.format(stack))
    except sdk.exceptions.OpenStackCloudException as e:
        if hasattr(e, 'response'):
            module.fail_json(msg=to_native(e), response=e.response.json())
        else:
            module.fail_json(msg=to_native(e))
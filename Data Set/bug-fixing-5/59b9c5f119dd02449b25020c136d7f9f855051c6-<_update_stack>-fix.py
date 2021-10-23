def _update_stack(module, stack, cloud, shade):
    try:
        stack = cloud.update_stack(module.params['name'], template_file=module.params['template'], environment_files=module.params['environment'], timeout=module.params['timeout'], rollback=module.params['rollback'], wait=module.params['wait'], **module.params['parameters'])
        if (stack['stack_status'] == 'UPDATE_COMPLETE'):
            return stack
        else:
            module.fail_json(msg=('Failure in updating stack: %s' % stack['stack_status_reason']))
    except shade.OpenStackCloudException as e:
        if hasattr(e, 'response'):
            module.fail_json(msg=to_native(e), response=e.response.json())
        else:
            module.fail_json(msg=to_native(e))
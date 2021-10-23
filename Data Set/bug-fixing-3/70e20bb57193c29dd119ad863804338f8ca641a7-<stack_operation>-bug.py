def stack_operation(cfn, stack_name, operation):
    'gets the status of a stack while it is created/updated/deleted'
    existed = []
    while True:
        try:
            stack = get_stack_facts(cfn, stack_name)
            existed.append('yes')
        except:
            if (('yes' in existed) or (operation == 'DELETE')):
                ret = get_stack_events(cfn, stack_name)
                ret.update({
                    'changed': True,
                    'output': 'Stack Deleted',
                })
                return ret
            else:
                return {
                    'changed': True,
                    'failed': True,
                    'output': 'Stack Not Found',
                    'exception': traceback.format_exc(),
                }
        ret = get_stack_events(cfn, stack_name)
        if (not stack):
            if (('yes' in existed) or (operation == 'DELETE')):
                ret = get_stack_events(cfn, stack_name)
                ret.update({
                    'changed': True,
                    'output': 'Stack Deleted',
                })
                return ret
            else:
                ret.update({
                    'changed': False,
                    'failed': True,
                    'output': 'Stack not found.',
                })
                return ret
        elif stack['StackStatus'].endswith('ROLLBACK_COMPLETE'):
            ret.update({
                'changed': True,
                'failed': True,
                'output': ('Problem with %s. Rollback complete' % operation),
            })
            return ret
        elif stack['StackStatus'].endswith('_COMPLETE'):
            ret.update({
                'changed': True,
                'output': ('Stack %s complete' % operation),
            })
            return ret
        elif stack['StackStatus'].endswith('_ROLLBACK_FAILED'):
            ret.update({
                'changed': True,
                'failed': True,
                'output': ('Stack %s rollback failed' % operation),
            })
            return ret
        elif stack['StackStatus'].endswith('_FAILED'):
            ret.update({
                'changed': True,
                'failed': True,
                'output': ('Stack %s failed' % operation),
            })
            return ret
        else:
            time.sleep(5)
    return {
        'failed': True,
        'output': 'Failed for unknown reasons.',
    }
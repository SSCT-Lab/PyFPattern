def perform_action(self, resource, definition):
    result = {
        'changed': False,
        'result': {
            
        },
    }
    state = self.params.get('state', None)
    force = self.params.get('force', False)
    name = definition['metadata'].get('name')
    namespace = definition['metadata'].get('namespace')
    existing = None
    self.remove_aliases()
    if definition['kind'].endswith('list'):
        result['result'] = resource.get(namespace=namespace).to_dict()
        result['changed'] = False
        result['method'] = 'get'
        return result
    try:
        existing = resource.get(name=name, namespace=namespace)
    except NotFoundError:
        pass
    except DynamicApiError as exc:
        self.fail_json(msg='Failed to retrieve requested object: {0}'.format(exc.body), error=exc.status, status=exc.status, reason=exc.reason)
    if (state == 'absent'):
        result['method'] = 'delete'
        if (not existing):
            return result
        else:
            if (not self.check_mode):
                try:
                    k8s_obj = resource.delete(name, namespace=namespace)
                    result['result'] = k8s_obj.to_dict()
                except DynamicApiError as exc:
                    self.fail_json(msg='Failed to delete object: {0}'.format(exc.body), error=exc.status, status=exc.status, reason=exc.reason)
            result['changed'] = True
            return result
    else:
        if (not existing):
            if self.check_mode:
                k8s_obj = definition
            else:
                try:
                    k8s_obj = resource.create(definition, namespace=namespace).to_dict()
                except ConflictError:
                    self.warn('{0} was not found, but creating it returned a 409 Conflict error. This can happen                                   if the resource you are creating does not directly create a resource of the same kind.'.format(name))
                    return result
            result['result'] = k8s_obj
            result['changed'] = True
            result['method'] = 'create'
            return result
        match = False
        diffs = []
        if (existing and force):
            if self.check_mode:
                k8s_obj = definition
            else:
                try:
                    k8s_obj = resource.replace(definition, name=name, namespace=namespace).to_dict()
                except DynamicApiError as exc:
                    self.fail_json(msg='Failed to replace object: {0}'.format(exc.body), error=exc.status, status=exc.status, reason=exc.reason)
            (match, diffs) = self.diff_objects(existing.to_dict(), k8s_obj)
            result['result'] = k8s_obj
            result['changed'] = (not match)
            result['method'] = 'replace'
            result['diff'] = diffs
            return result
        if self.check_mode:
            k8s_obj = dict_merge(existing.to_dict(), definition)
        else:
            try:
                k8s_obj = resource.patch(definition, name=name, namespace=namespace).to_dict()
            except DynamicApiError as exc:
                self.fail_json(msg='Failed to patch object: {0}'.format(exc.body), error=exc.status, status=exc.status, reason=exc.reason)
        (match, diffs) = self.diff_objects(existing.to_dict(), k8s_obj)
        result['result'] = k8s_obj
        result['changed'] = (not match)
        result['method'] = 'patch'
        result['diff'] = diffs
        return result
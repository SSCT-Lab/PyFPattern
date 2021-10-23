

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
    wait = self.params.get('wait')
    wait_sleep = self.params.get('wait_sleep')
    wait_timeout = self.params.get('wait_timeout')
    wait_condition = None
    if (self.params.get('wait_condition') and self.params['wait_condition'].get('type')):
        wait_condition = self.params['wait_condition']
    self.remove_aliases()
    try:
        if (self.append_hash and (definition['kind'] in ['ConfigMap', 'Secret'])):
            name = ('%s-%s' % (name, generate_hash(definition)))
            definition['metadata']['name'] = name
        params = dict(name=name)
        if namespace:
            params['namespace'] = namespace
        existing = resource.get(**params)
    except NotFoundError:
        try:
            sys.exc_clear()
        except AttributeError:
            pass
    except ForbiddenError as exc:
        if ((definition['kind'] in ['Project', 'ProjectRequest']) and (state != 'absent')):
            return self.create_project_request(definition)
        self.fail_json(msg='Failed to retrieve requested object: {0}'.format(exc.body), error=exc.status, status=exc.status, reason=exc.reason)
    except DynamicApiError as exc:
        self.fail_json(msg='Failed to retrieve requested object: {0}'.format(exc.body), error=exc.status, status=exc.status, reason=exc.reason)
    if (state == 'absent'):
        result['method'] = 'delete'
        if (not existing):
            return result
        else:
            result['changed'] = True
            if (not self.check_mode):
                try:
                    k8s_obj = resource.delete(**params)
                    result['result'] = k8s_obj.to_dict()
                except DynamicApiError as exc:
                    self.fail_json(msg='Failed to delete object: {0}'.format(exc.body), error=exc.status, status=exc.status, reason=exc.reason)
                if wait:
                    (success, resource, duration) = self.wait(resource, definition, wait_sleep, wait_timeout, 'absent')
                    result['duration'] = duration
                    if (not success):
                        self.fail_json(msg='Resource deletion timed out', **result)
            return result
    else:
        if self.apply:
            if self.check_mode:
                k8s_obj = definition
            else:
                try:
                    k8s_obj = resource.apply(definition, namespace=namespace).to_dict()
                except DynamicApiError as exc:
                    msg = 'Failed to apply object: {0}'.format(exc.body)
                    if self.warnings:
                        msg += ('\n' + '\n    '.join(self.warnings))
                    self.fail_json(msg=msg, error=exc.status, status=exc.status, reason=exc.reason)
            success = True
            result['result'] = k8s_obj
            if wait:
                (success, result['result'], result['duration']) = self.wait(resource, definition, wait_sleep, wait_timeout)
            if existing:
                existing = existing.to_dict()
            else:
                existing = {
                    
                }
            (match, diffs) = self.diff_objects(existing, result['result'])
            result['changed'] = (not match)
            result['diff'] = diffs
            result['method'] = 'apply'
            if (not success):
                self.fail_json(msg='Resource apply timed out', **result)
            return result
        if (not existing):
            if self.check_mode:
                k8s_obj = definition
            else:
                try:
                    k8s_obj = resource.create(definition, namespace=namespace).to_dict()
                except ConflictError:
                    self.warn('{0} was not found, but creating it returned a 409 Conflict error. This can happen                                   if the resource you are creating does not directly create a resource of the same kind.'.format(name))
                    return result
                except DynamicApiError as exc:
                    msg = 'Failed to create object: {0}'.format(exc.body)
                    if self.warnings:
                        msg += ('\n' + '\n    '.join(self.warnings))
                    self.fail_json(msg=msg, error=exc.status, status=exc.status, reason=exc.reason)
            success = True
            result['result'] = k8s_obj
            if (wait and (not self.check_mode)):
                (success, result['result'], result['duration']) = self.wait(resource, definition, wait_sleep, wait_timeout, condition=wait_condition)
            result['changed'] = True
            result['method'] = 'create'
            if (not success):
                self.fail_json(msg='Resource creation timed out', **result)
            return result
        match = False
        diffs = []
        if (existing and force):
            if self.check_mode:
                k8s_obj = definition
            else:
                try:
                    k8s_obj = resource.replace(definition, name=name, namespace=namespace, append_hash=self.append_hash).to_dict()
                except DynamicApiError as exc:
                    msg = 'Failed to replace object: {0}'.format(exc.body)
                    if self.warnings:
                        msg += ('\n' + '\n    '.join(self.warnings))
                    self.fail_json(msg=msg, error=exc.status, status=exc.status, reason=exc.reason)
            (match, diffs) = self.diff_objects(existing.to_dict(), k8s_obj)
            success = True
            result['result'] = k8s_obj
            if wait:
                (success, result['result'], result['duration']) = self.wait(resource, definition, wait_sleep, wait_timeout, condition=wait_condition)
            (match, diffs) = self.diff_objects(existing.to_dict(), result['result'])
            result['changed'] = (not match)
            result['method'] = 'replace'
            result['diff'] = diffs
            if (not success):
                self.fail_json(msg='Resource replacement timed out', **result)
            return result
        if self.check_mode:
            k8s_obj = dict_merge(existing.to_dict(), definition)
        else:
            if (LooseVersion(self.openshift_version) < LooseVersion('0.6.2')):
                (k8s_obj, error) = self.patch_resource(resource, definition, existing, name, namespace)
            else:
                for merge_type in (self.params['merge_type'] or ['strategic-merge', 'merge']):
                    (k8s_obj, error) = self.patch_resource(resource, definition, existing, name, namespace, merge_type=merge_type)
                    if (not error):
                        break
            if error:
                self.fail_json(**error)
        success = True
        result['result'] = k8s_obj
        if wait:
            (success, result['result'], result['duration']) = self.wait(resource, definition, wait_sleep, wait_timeout, condition=wait_condition)
        (match, diffs) = self.diff_objects(existing.to_dict(), result['result'])
        result['changed'] = (not match)
        result['method'] = 'patch'
        result['diff'] = diffs
        if (not success):
            self.fail_json(msg='Resource update timed out', **result)
        return result

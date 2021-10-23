def _wait_for(self, resource, name, namespace, predicate, timeout, state):
    start = datetime.now()

    def _wait_for_elapsed():
        return (datetime.now() - start).seconds
    response = None
    while (_wait_for_elapsed() < timeout):
        try:
            response = resource.get(name=name, namespace=namespace)
            if predicate(response):
                if response:
                    return (True, response.to_dict(), _wait_for_elapsed())
                else:
                    return (True, {
                        
                    }, _wait_for_elapsed())
            time.sleep((timeout // 20))
        except NotFoundError:
            if (state == 'absent'):
                return (True, {
                    
                }, _wait_for_elapsed())
    if response:
        response = response.to_dict()
    return (False, response, _wait_for_elapsed())
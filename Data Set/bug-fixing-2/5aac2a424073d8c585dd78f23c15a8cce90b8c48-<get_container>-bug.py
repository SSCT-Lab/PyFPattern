

def get_container(self, name=None):
    '\n        Lookup a container and return the inspection results.\n        '
    if (name is None):
        return None
    search_name = name
    if (not name.startswith('/')):
        search_name = ('/' + name)
    result = None
    try:
        for container in self.containers(all=True):
            self.log(('testing container: %s' % container['Names']))
            if (search_name in container['Names']):
                result = container
                break
            if container['Id'].startswith(name):
                result = container
                break
            if (container['Id'] == name):
                result = container
                break
    except SSLError as exc:
        self._handle_ssl_error(exc)
    except Exception as exc:
        self.fail(('Error retrieving container list: %s' % exc))
    if (result is not None):
        try:
            self.log(('Inspecting container Id %s' % result['Id']))
            result = self.inspect_container(container=result['Id'])
            self.log('Completed container inspection')
        except Exception as exc:
            self.fail(('Error inspecting container: %s' % exc))
    return result

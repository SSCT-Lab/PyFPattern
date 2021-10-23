def handle_request(self, request):
    request = json.loads(to_text(request, errors='surrogate_then_replace'))
    method = request.get('method')
    if (method.startswith('rpc.') or method.startswith('_')):
        error = self.invalid_request()
        return json.dumps(error)
    (args, kwargs) = request.get('params')
    setattr(self, '_identifier', request.get('id'))
    rpc_method = None
    for obj in self._objects:
        rpc_method = getattr(obj, method, None)
        if rpc_method:
            break
    if (not rpc_method):
        error = self.method_not_found()
        response = json.dumps(error)
    else:
        try:
            result = rpc_method(*args, **kwargs)
        except ConnectionError as exc:
            display.vvv(traceback.format_exc())
            try:
                error = self.error(code=exc.code, message=to_text(exc))
            except AttributeError:
                error = self.internal_error(data=to_text(exc))
            response = json.dumps(error)
        except Exception as exc:
            display.vvv(traceback.format_exc())
            error = self.internal_error(data=to_text(exc, errors='surrogate_then_replace'))
            response = json.dumps(error)
        else:
            if (isinstance(result, dict) and ('jsonrpc' in result)):
                response = result
            else:
                response = self.response(result)
            response = json.dumps(response)
    delattr(self, '_identifier')
    return response
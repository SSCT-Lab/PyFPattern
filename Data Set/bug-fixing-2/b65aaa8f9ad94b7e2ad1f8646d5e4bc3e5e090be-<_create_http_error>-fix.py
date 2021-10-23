

@staticmethod
def _create_http_error(response):
    '\n        :type response: HttpResponse\n        :rtype: ApplicationError\n        '
    response_json = response.json()
    stack_trace = ''
    if ('message' in response_json):
        message = response_json['message']
    elif ('errorMessage' in response_json):
        message = response_json['errorMessage'].strip()
        if ('stackTrace' in response_json):
            traceback_lines = response_json['stackTrace']
            if (traceback_lines and isinstance(traceback_lines[0], list)):
                traceback_lines = traceback.format_list(traceback_lines)
            trace = '\n'.join([x.rstrip() for x in traceback_lines])
            stack_trace = ('\nTraceback (from remote server):\n%s' % trace)
    else:
        message = str(response_json)
    return CoreHttpError(response.status_code, message, stack_trace)

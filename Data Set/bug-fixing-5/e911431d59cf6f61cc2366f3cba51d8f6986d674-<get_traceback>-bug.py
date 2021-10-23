def get_traceback(self, event, context):
    result = [event.message, '', ('File "%s", line %s' % (self.filename, self.lineno)), '']
    result.extend([n[1].strip('\n') for n in context])
    return '\n'.join(result)
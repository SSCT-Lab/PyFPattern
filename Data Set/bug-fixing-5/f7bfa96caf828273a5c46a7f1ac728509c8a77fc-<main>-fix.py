def main():
    'Main program function.'
    base_dir = os.getcwd()
    messages = set()
    for path in sys.argv[1:]:
        try:
            with open(path, 'r') as module_fd:
                imp.load_module('module_import_test', module_fd, os.path.abspath(path), ('.py', 'r', imp.PY_SOURCE))
        except Exception as ex:
            (exc_type, _, exc_tb) = sys.exc_info()
            message = str(ex)
            results = list(reversed(traceback.extract_tb(exc_tb)))
            source = None
            line = 0
            offset = 0
            for result in results:
                if result[0].startswith(base_dir):
                    source = result[0][(len(base_dir) + 1):].replace('test/runner/import/', '')
                    line = (result[1] or 0)
                    break
            if (not source):
                source = path
                message += (' (in %s:%d)' % (results[(- 1)][0], (results[(- 1)][1] or 0)))
            elif isinstance(ex, SyntaxError):
                if ex.filename.endswith(path):
                    source = path
                    line = (ex.lineno or 0)
                    offset = (ex.offset or 0)
                    message = str(ex)
                    message = message.replace((' (%s, line %d)' % (os.path.basename(path), line)), '')
            error = ('%s:%d:%d: %s: %s' % (source, line, offset, exc_type.__name__, message))
            if (error not in messages):
                messages.add(error)
                print(error)
    if messages:
        exit(10)
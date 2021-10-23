

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
            line = None
            for result in results:
                if result[0].startswith(base_dir):
                    source = result[0][(len(base_dir) + 1):].replace('test/runner/import/', '')
                    line = result[1]
                    break
            if (not source):
                source = path
                line = 0
                message += (' (in %s:%d)' % (results[(- 1)][0], results[(- 1)][1]))
            error = ('%s:%d:0: %s: %s' % (source, line, exc_type.__name__, message))
            if (error not in messages):
                messages.add(error)
                print(error)
    if messages:
        exit(10)

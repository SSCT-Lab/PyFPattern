def test_python_module(path, base_dir, messages, ansible_module):
    if ansible_module:
        if (sys.version_info < (2, 7)):
            return
        if (not path.startswith('lib/ansible/modules/')):
            return
        if (path == 'lib/ansible/modules/utilities/logic/async_wrapper.py'):
            return
        name = '__main__'
        filter_dir = os.path.join(base_dir, 'lib/ansible/modules')
    else:
        name = 'module_import_test'
        filter_dir = base_dir
    capture = Capture()
    try:
        with open(path, 'r') as module_fd:
            with capture_output(capture):
                imp.load_module(name, module_fd, os.path.abspath(path), ('.py', 'r', imp.PY_SOURCE))
        capture_report(path, capture, messages)
    except ImporterAnsibleModuleException:
        pass
    except BaseException as ex:
        capture_report(path, capture, messages)
        (exc_type, _, exc_tb) = sys.exc_info()
        message = str(ex)
        results = list(reversed(traceback.extract_tb(exc_tb)))
        source = None
        line = 0
        offset = 0
        for result in results:
            if result[0].startswith(filter_dir):
                source = result[0][(len(base_dir) + 1):].replace('test/sanity/import/', '')
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
        message = re.sub('\\n *', ': ', message)
        error = ('%s:%d:%d: %s: %s' % (source, line, offset, exc_type.__name__, message))
        report_message(error, messages)
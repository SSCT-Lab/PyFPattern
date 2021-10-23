def main():
    '\n    Main program function used to isolate globals from imported code.\n    Changes to globals in imported modules on Python 2.7 will overwrite our own globals.\n    '
    import contextlib
    import os
    import re
    import sys
    import traceback
    import warnings
    try:
        import importlib.util
        imp = None
    except ImportError:
        importlib = None
        import imp
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO
    import ansible.module_utils.basic
    import ansible.module_utils.common.removed
    try:
        from ansible.utils.collection_loader import AnsibleCollectionLoader
    except ImportError:
        AnsibleCollectionLoader = None

    class ImporterAnsibleModuleException(Exception):
        'Exception thrown during initialization of ImporterAnsibleModule.'

    class ImporterAnsibleModule():
        'Replacement for AnsibleModule to support import testing.'

        def __init__(self, *args, **kwargs):
            raise ImporterAnsibleModuleException()
    ansible.module_utils.basic.AnsibleModule = ImporterAnsibleModule
    ansible.module_utils.basic._load_params = (lambda *args, **kwargs: {
        
    })
    ansible.module_utils.common.removed.removed_module = (lambda *args, **kwargs: None)

    def run():
        'Main program function.'
        base_dir = os.getcwd()
        messages = set()
        if AnsibleCollectionLoader:
            sys.meta_path.insert(0, AnsibleCollectionLoader())
        for path in (sys.argv[1:] or sys.stdin.read().splitlines()):
            test_python_module(path, base_dir, messages, False)
            test_python_module(path, base_dir, messages, True)
        if messages:
            exit(10)

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
            if imp:
                with open(path, 'r') as module_fd:
                    with capture_output(capture):
                        imp.load_module(name, module_fd, os.path.abspath(path), ('.py', 'r', imp.PY_SOURCE))
            else:
                spec = importlib.util.spec_from_file_location(name, os.path.abspath(path))
                module = importlib.util.module_from_spec(spec)
                with capture_output(capture):
                    spec.loader.exec_module(module)
            capture_report(path, capture, messages)
        except ImporterAnsibleModuleException:
            pass
        except BaseException as ex:
            capture_report(path, capture, messages)
            (exc_type, _exc, exc_tb) = sys.exc_info()
            message = str(ex)
            results = list(reversed(traceback.extract_tb(exc_tb)))
            source = None
            line = 0
            offset = 0
            if (isinstance(ex, SyntaxError) and ex.filename.endswith(path)):
                source = path
                line = (ex.lineno or 0)
                offset = (ex.offset or 0)
                message = str(ex)
                message = message.replace((' (%s, line %d)' % (os.path.basename(path), line)), '')
            else:
                for result in results:
                    if result[0].startswith(filter_dir):
                        source = result[0][(len(base_dir) + 1):].replace('test/sanity/import/', '')
                        line = (result[1] or 0)
                        break
                if (not source):
                    source = path
                    message += (' (in %s:%d)' % (results[(- 1)][0], (results[(- 1)][1] or 0)))
            message = re.sub('\\n *', ': ', message)
            error = ('%s:%d:%d: %s: %s' % (source, line, offset, exc_type.__name__, message))
            report_message(error, messages)

    class Capture():
        'Captured output and/or exception.'

        def __init__(self):
            self.stdout = StringIO()
            self.stderr = StringIO()
            self.warnings = []

    def capture_report(path, capture, messages):
        'Report on captured output.\n        :type path: str\n        :type capture: Capture\n        :type messages: set[str]\n        '
        if capture.stdout.getvalue():
            first = capture.stdout.getvalue().strip().splitlines()[0].strip()
            message = ('%s:%d:%d: %s: %s' % (path, 0, 0, 'StandardOutputUsed', first))
            report_message(message, messages)
        if capture.stderr.getvalue():
            first = capture.stderr.getvalue().strip().splitlines()[0].strip()
            message = ('%s:%d:%d: %s: %s' % (path, 0, 0, 'StandardErrorUsed', first))
            report_message(message, messages)
        for warning in capture.warnings:
            msg = re.sub('\\s+', ' ', ('%s' % warning.message)).strip()
            filepath = os.path.relpath(warning.filename)
            lineno = warning.lineno
            import_dir = 'test/runner/.tox/import/'
            minimal_dir = 'test/runner/.tox/minimal-'
            if (filepath.startswith('../') or filepath.startswith(minimal_dir)):
                msg += (' (in %s:%d)' % (warning.filename, warning.lineno))
                filepath = path
                lineno = 0
            elif filepath.startswith(import_dir):
                filepath = os.path.relpath(filepath, import_dir)
            message = ('%s:%d:%d: %s: %s' % (filepath, lineno, 0, warning.category.__name__, msg))
            report_message(message, messages)

    def report_message(message, messages):
        'Report message if not already reported.\n        :type message: str\n        :type messages: set[str]\n        '
        if (message not in messages):
            messages.add(message)
            print(message)

    @contextlib.contextmanager
    def capture_output(capture):
        'Capture sys.stdout and sys.stderr.\n        :type capture: Capture\n        '
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = capture.stdout
        sys.stderr = capture.stderr
        with warnings.catch_warnings(record=True) as captured_warnings:
            try:
                (yield)
            finally:
                capture.warnings = captured_warnings
                sys.stdout = old_stdout
                sys.stderr = old_stderr
    run()
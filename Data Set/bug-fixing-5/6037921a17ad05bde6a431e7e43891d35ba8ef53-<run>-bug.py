def run(file_list=None, format=True, lint=True, js=True, py=True, less=True, yarn=True, test=False, parseable=False):
    old_sysargv = sys.argv
    try:
        sys.argv = [os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir)]
        results = []
        if yarn:
            results.append(yarn_check(file_list))
        if any(results):
            return 1
        if format:
            if py:
                results.append(py_format(file_list))
            if js:
                results.append(js_lint_format(file_list))
                results.append(js_format(file_list))
            if less:
                results.append(less_format(file_list))
        if any(results):
            return 1
        if lint:
            if py:
                raise NotImplementedError('flake8 linting was moved to pre-commit hooks.')
            if js:
                results.append(js_stylelint(file_list, parseable=parseable, format=format))
                if (not format):
                    results.append(js_lint(file_list, parseable=parseable, format=format))
        if test:
            if js:
                results.append(js_test(file_list))
        if any(results):
            return 1
        return 0
    finally:
        sys.argv = old_sysargv
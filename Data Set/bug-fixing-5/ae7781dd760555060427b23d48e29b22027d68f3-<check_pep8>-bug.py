def check_pep8(files):

    def run_pycodestyle(files, ignored_rules):
        failed = False
        pep8 = subprocess.Popen(((['pycodestyle'] + files) + ['--ignore={rules}'.format(rules=','.join(ignored_rules))]), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        for pipe in (pep8.stdout, pep8.stderr):
            assert (pipe is not None)
            for ln in pipe:
                sys.stdout.write(ln)
                failed = True
        return failed
    failed = False
    ignored_rules = ['E221', 'E226', 'E251', 'E265', 'E266', 'E302', 'E305', 'E402', 'E501', 'E731']
    IGNORE_FILES_PEPE261 = ['api/zulip/__init__.py', 'tools/run-dev.py', 'zerver/lib/bugdown/__init__.py', 'zerver/models.py', 'zerver/tests/test_bugdown.py', 'zerver/tests/test_events.py', 'zerver/tests/test_messages.py', 'zerver/tests/test_narrow.py', 'zerver/tests/test_outgoing_webhook_system.py', 'zerver/tests/test_realm.py', 'zerver/tests/test_signup.py', 'zerver/tests/test_subs.py', 'zerver/tests/test_upload.py', 'zerver/tornado/socket.py', 'zerver/tornado/websocket_client.py', 'zerver/worker/queue_processors.py', 'zilencer/management/commands/populate_db.py', 'zproject/dev_settings.py', 'zproject/prod_settings_template.py', 'zproject/settings.py']
    filtered_files = [fn for fn in files if (fn not in IGNORE_FILES_PEPE261)]
    filtered_files_E261 = [fn for fn in files if (fn in IGNORE_FILES_PEPE261)]
    if (len(files) == 0):
        return False
    if (not (len(filtered_files) == 0)):
        failed = run_pycodestyle(filtered_files, ignored_rules)
    if (not (len(filtered_files_E261) == 0)):
        if (not failed):
            failed = run_pycodestyle(filtered_files_E261, (ignored_rules + ['E261']))
    return failed
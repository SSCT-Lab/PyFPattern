def main(options: argparse.Namespace) -> int:
    setup_bash_profile()
    setup_shell_profile('~/.zprofile')
    run(['scripts/setup/generate_secrets.py', '--development'])
    os.makedirs(LOG_DIR_PATH, exist_ok=True)
    os.makedirs(UPLOAD_DIR_PATH, exist_ok=True)
    os.makedirs(TEST_UPLOAD_DIR_PATH, exist_ok=True)
    os.makedirs(COVERAGE_DIR_PATH, exist_ok=True)
    os.makedirs(NODE_TEST_COVERAGE_DIR_PATH, exist_ok=True)
    os.makedirs(XUNIT_XML_TEST_RESULTS_DIR_PATH, exist_ok=True)
    if (not os.access(EMOJI_CACHE_PATH, os.W_OK)):
        run_as_root(['mkdir', '-p', EMOJI_CACHE_PATH])
        run_as_root(['chown', ('%s:%s' % (os.getuid(), os.getgid())), EMOJI_CACHE_PATH])
    run(['tools/setup/emoji/build_emoji'])
    generate_zulip_bots_static_files()
    build_pygments_data_paths = ['tools/setup/build_pygments_data', 'tools/setup/lang.json']
    from pygments import __version__ as pygments_version
    if file_or_package_hash_updated(build_pygments_data_paths, 'build_pygments_data_hash', options.is_force, [pygments_version]):
        run(['tools/setup/build_pygments_data'])
    else:
        print('No need to run `tools/setup/build_pygments_data`.')
    update_authors_json_paths = ['tools/update-authors-json', 'zerver/tests/fixtures/authors.json']
    if file_or_package_hash_updated(update_authors_json_paths, 'update_authors_json_hash', options.is_force):
        run(['tools/update-authors-json', '--use-fixture'])
    else:
        print('No need to run `tools/update-authors-json`.')
    email_source_paths = ['tools/inline-email-css', 'templates/zerver/emails/email.css']
    email_source_paths += glob.glob('templates/zerver/emails/*.source.html')
    if file_or_package_hash_updated(email_source_paths, 'last_email_source_files_hash', options.is_force):
        run(['tools/inline-email-css'])
    else:
        print('No need to run `tools/inline-email-css`.')
    if (not options.is_production_travis):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zproject.settings')
        import django
        django.setup()
        from zerver.lib.test_fixtures import template_database_status, run_db_migrations, destroy_leaked_test_databases
        try:
            from zerver.lib.queue import SimpleQueueClient
            SimpleQueueClient()
            rabbitmq_is_configured = True
        except Exception:
            rabbitmq_is_configured = False
        if (options.is_force or (not rabbitmq_is_configured)):
            run(['scripts/setup/configure-rabbitmq'])
        else:
            print('RabbitMQ is already configured.')
        migration_status_path = os.path.join(UUID_VAR_PATH, 'migration_status_dev')
        dev_template_db_status = template_database_status(migration_status=migration_status_path, settings='zproject.settings', database_name='zulip')
        if (options.is_force or (dev_template_db_status == 'needs_rebuild')):
            run(['tools/setup/postgres-init-dev-db'])
            run(['tools/do-destroy-rebuild-database'])
        elif (dev_template_db_status == 'run_migrations'):
            run_db_migrations('dev')
        elif (dev_template_db_status == 'current'):
            print('No need to regenerate the dev DB.')
        test_template_db_status = template_database_status()
        if (options.is_force or (test_template_db_status == 'needs_rebuild')):
            run(['tools/setup/postgres-init-test-db'])
            run(['tools/do-destroy-rebuild-test-database'])
        elif (test_template_db_status == 'run_migrations'):
            run_db_migrations('test')
        elif (test_template_db_status == 'current'):
            print('No need to regenerate the test DB.')
        paths = ['zerver/management/commands/compilemessages.py']
        paths += glob.glob('locale/*/LC_MESSAGES/*.po')
        paths += glob.glob('locale/*/translations.json')
        if file_or_package_hash_updated(paths, 'last_compilemessages_hash', options.is_force):
            run(['./manage.py', 'compilemessages'])
        else:
            print('No need to run `manage.py compilemessages`.')
        destroyed = destroy_leaked_test_databases()
        if destroyed:
            print(('Dropped %s stale test databases!' % (destroyed,)))
    run(['scripts/lib/clean-unused-caches', '--threshold=6'])
    if os.path.isfile('.eslintcache'):
        os.remove('.eslintcache')
    print('Cleaning var/ directory files...')
    var_paths = glob.glob('var/test*')
    var_paths.append('var/bot_avatar')
    for path in var_paths:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except FileNotFoundError:
            pass
    version_file = os.path.join(UUID_VAR_PATH, 'provision_version')
    print(('writing to %s\n' % (version_file,)))
    open(version_file, 'w').write((PROVISION_VERSION + '\n'))
    print()
    print(((OKBLUE + 'Zulip development environment setup succeeded!') + ENDC))
    return 0
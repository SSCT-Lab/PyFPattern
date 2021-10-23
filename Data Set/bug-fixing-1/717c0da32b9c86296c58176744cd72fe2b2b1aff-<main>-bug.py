

def main():
    argument_spec = url_argument_spec()
    argument_spec.update(add_export_distributor=dict(default=False, type='bool'), feed=dict(), generate_sqlite=dict(default=False, type='bool'), feed_ca_cert=dict(aliases=['importer_ssl_ca_cert', 'ca_cert'], deprecated_aliases=[dict(name='ca_cert', version='2.14')]), feed_client_cert=dict(aliases=['importer_ssl_client_cert']), feed_client_key=dict(aliases=['importer_ssl_client_key']), name=dict(required=True, aliases=['repo']), proxy_host=dict(), proxy_port=dict(), proxy_username=dict(), proxy_password=dict(no_log=True), publish_distributor=dict(), pulp_host=dict(default='https://127.0.0.1'), relative_url=dict(), repo_type=dict(default='rpm'), repoview=dict(default=False, type='bool'), serve_http=dict(default=False, type='bool'), serve_https=dict(default=True, type='bool'), state=dict(default='present', choices=['absent', 'present', 'sync', 'publish']), wait_for_completion=dict(default=False, type='bool'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    add_export_distributor = module.params['add_export_distributor']
    feed = module.params['feed']
    generate_sqlite = module.params['generate_sqlite']
    importer_ssl_ca_cert = module.params['feed_ca_cert']
    importer_ssl_client_cert = module.params['feed_client_cert']
    if ((importer_ssl_client_cert is None) and (module.params['client_cert'] is not None)):
        importer_ssl_client_cert = module.params['client_cert']
        module.deprecate('To specify client certificates to be used with the repo to sync, and not for communication with the Pulp instance, use the new options `feed_client_cert` and `feed_client_key` (available since Ansible 2.10). Until Ansible 2.14, the default value for `feed_client_cert` will be taken from `client_cert` if only the latter is specified', version='2.14')
    importer_ssl_client_key = module.params['feed_client_key']
    if ((importer_ssl_client_key is None) and (module.params['client_key'] is not None)):
        importer_ssl_client_key = module.params['client_key']
        module.deprecate('In Ansible 2.10 `feed_client_key` option was added. Until 2.14 the default value will come from client_key option', version='2.14')
    proxy_host = module.params['proxy_host']
    proxy_port = module.params['proxy_port']
    proxy_username = module.params['proxy_username']
    proxy_password = module.params['proxy_password']
    publish_distributor = module.params['publish_distributor']
    pulp_host = module.params['pulp_host']
    relative_url = module.params['relative_url']
    repo = module.params['name']
    repo_type = module.params['repo_type']
    repoview = module.params['repoview']
    serve_http = module.params['serve_http']
    serve_https = module.params['serve_https']
    state = module.params['state']
    wait_for_completion = module.params['wait_for_completion']
    if ((state == 'present') and (not relative_url)):
        module.fail_json(msg='When state is present, relative_url is required.')
    if (importer_ssl_ca_cert is not None):
        importer_ssl_ca_cert_file_path = os.path.abspath(importer_ssl_ca_cert)
        if os.path.isfile(importer_ssl_ca_cert_file_path):
            importer_ssl_ca_cert_file_object = open(importer_ssl_ca_cert_file_path, 'r')
            try:
                importer_ssl_ca_cert = importer_ssl_ca_cert_file_object.read()
            finally:
                importer_ssl_ca_cert_file_object.close()
    if (importer_ssl_client_cert is not None):
        importer_ssl_client_cert_file_path = os.path.abspath(importer_ssl_client_cert)
        if os.path.isfile(importer_ssl_client_cert_file_path):
            importer_ssl_client_cert_file_object = open(importer_ssl_client_cert_file_path, 'r')
            try:
                importer_ssl_client_cert = importer_ssl_client_cert_file_object.read()
            finally:
                importer_ssl_client_cert_file_object.close()
    if (importer_ssl_client_key is not None):
        importer_ssl_client_key_file_path = os.path.abspath(importer_ssl_client_key)
        if os.path.isfile(importer_ssl_client_key_file_path):
            importer_ssl_client_key_file_object = open(importer_ssl_client_key_file_path, 'r')
            try:
                importer_ssl_client_key = importer_ssl_client_key_file_object.read()
            finally:
                importer_ssl_client_key_file_object.close()
    server = pulp_server(module, pulp_host, repo_type, wait_for_completion=wait_for_completion)
    server.set_repo_list()
    repo_exists = server.check_repo_exists(repo)
    changed = False
    if ((state == 'absent') and repo_exists):
        if (not module.check_mode):
            server.delete_repo(repo)
        changed = True
    if (state == 'sync'):
        if (not repo_exists):
            module.fail_json(msg='Repository was not found. The repository can not be synced.')
        if (not module.check_mode):
            server.sync_repo(repo)
        changed = True
    if (state == 'publish'):
        if (not repo_exists):
            module.fail_json(msg='Repository was not found. The repository can not be published.')
        if (not module.check_mode):
            server.publish_repo(repo, publish_distributor)
        changed = True
    if (state == 'present'):
        if (not repo_exists):
            if (not module.check_mode):
                server.create_repo(repo_id=repo, relative_url=relative_url, feed=feed, generate_sqlite=generate_sqlite, serve_http=serve_http, serve_https=serve_https, proxy_host=proxy_host, proxy_port=proxy_port, proxy_username=proxy_username, proxy_password=proxy_password, repoview=repoview, ssl_ca_cert=importer_ssl_ca_cert, ssl_client_cert=importer_ssl_client_cert, ssl_client_key=importer_ssl_client_key, add_export_distributor=add_export_distributor)
            changed = True
        else:
            if (not server.compare_repo_importer_config(repo, feed=feed, proxy_host=proxy_host, proxy_port=proxy_port, proxy_username=proxy_username, proxy_password=proxy_password, ssl_ca_cert=importer_ssl_ca_cert, ssl_client_cert=importer_ssl_client_cert, ssl_client_key=importer_ssl_client_key)):
                if (not module.check_mode):
                    server.update_repo_importer_config(repo, feed=feed, proxy_host=proxy_host, proxy_port=proxy_port, proxy_username=proxy_username, proxy_password=proxy_password, ssl_ca_cert=importer_ssl_ca_cert, ssl_client_cert=importer_ssl_client_cert, ssl_client_key=importer_ssl_client_key)
                changed = True
            if (relative_url is not None):
                if (not server.compare_repo_distributor_config(repo, relative_url=relative_url)):
                    if (not module.check_mode):
                        server.update_repo_distributor_config(repo, relative_url=relative_url)
                    changed = True
            if (not server.compare_repo_distributor_config(repo, generate_sqlite=generate_sqlite)):
                if (not module.check_mode):
                    server.update_repo_distributor_config(repo, generate_sqlite=generate_sqlite)
                changed = True
            if (not server.compare_repo_distributor_config(repo, repoview=repoview)):
                if (not module.check_mode):
                    server.update_repo_distributor_config(repo, repoview=repoview)
                changed = True
            if (not server.compare_repo_distributor_config(repo, http=serve_http)):
                if (not module.check_mode):
                    server.update_repo_distributor_config(repo, http=serve_http)
                changed = True
            if (not server.compare_repo_distributor_config(repo, https=serve_https)):
                if (not module.check_mode):
                    server.update_repo_distributor_config(repo, https=serve_https)
                changed = True
    module.exit_json(changed=changed, repo=repo)

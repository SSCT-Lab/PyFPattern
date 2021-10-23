def import_cert_url(module, executable, url, port, keystore_path, keystore_pass, alias, keystore_type, trust_cacert):
    ' Import certificate from URL into keystore located at keystore_path '
    https_proxy = os.getenv('https_proxy')
    no_proxy = os.getenv('no_proxy')
    proxy_opts = ''
    if (https_proxy is not None):
        (proxy_host, proxy_port) = https_proxy.split(':')
        proxy_opts = ('-J-Dhttps.proxyHost=%s -J-Dhttps.proxyPort=%s' % (proxy_host, proxy_port))
        if (no_proxy is not None):
            non_proxy_hosts = no_proxy.replace(',', '|')
            non_proxy_hosts = re.sub('(^|\\|)\\.', '\\1*.', non_proxy_hosts)
            proxy_opts += (" -J-Dhttp.nonProxyHosts='%s'" % non_proxy_hosts)
    fetch_cmd = ('%s -printcert -rfc -sslserver %s %s:%d' % (executable, proxy_opts, url, port))
    import_cmd = ("%s -importcert -noprompt -keystore '%s' -storepass '%s' -alias '%s' %s" % (executable, keystore_path, keystore_pass, alias, get_keystore_type(keystore_type)))
    if trust_cacert:
        import_cmd = (import_cmd + ' -trustcacerts')
    (_, fetch_out, _) = module.run_command(fetch_cmd, check_rc=True)
    (import_rc, import_out, import_err) = module.run_command(import_cmd, data=fetch_out, check_rc=False)
    diff = {
        'before': '\n',
        'after': ('%s\n' % alias),
    }
    if (import_rc == 0):
        module.exit_json(changed=True, msg=import_out, rc=import_rc, cmd=import_cmd, stdout=import_out, diff=diff)
    else:
        module.fail_json(msg=import_out, rc=import_rc, cmd=import_cmd, error=import_err)
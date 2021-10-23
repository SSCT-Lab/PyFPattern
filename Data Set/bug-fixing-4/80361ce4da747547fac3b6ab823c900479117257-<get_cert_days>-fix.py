def get_cert_days(module, cert_file):
    '\n    Return the days the certificate in cert_file remains valid and -1\n    if the file was not found.\n    '
    if (not os.path.exists(cert_file)):
        return (- 1)
    openssl_bin = module.get_bin_path('openssl', True)
    openssl_cert_cmd = [openssl_bin, 'x509', '-in', cert_file, '-noout', '-text']
    (_, out, _) = module.run_command(openssl_cert_cmd, check_rc=True, encoding=None)
    try:
        not_after_str = re.search('\\s+Not After\\s*:\\s+(.*)', out.decode('utf8')).group(1)
        not_after = datetime.fromtimestamp(time.mktime(time.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')))
    except AttributeError:
        module.fail_json(msg="No 'Not after' date found in {0}".format(cert_file))
    except ValueError:
        module.fail_json(msg="Failed to parse 'Not after' date of {0}".format(cert_file))
    now = datetime.utcnow()
    return (not_after - now).days
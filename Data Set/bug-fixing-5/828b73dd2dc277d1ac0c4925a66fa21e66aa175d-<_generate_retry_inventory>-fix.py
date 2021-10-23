def _generate_retry_inventory(self, retry_path, replay_hosts):
    '\n        Called when a playbook run fails. It generates an inventory which allows\n        re-running on ONLY the failed hosts.  This may duplicate some variable\n        information in group_vars/host_vars but that is ok, and expected.\n        '
    makedirs_safe(os.path.dirname(retry_path))
    try:
        with open(retry_path, 'w') as fd:
            for x in replay_hosts:
                fd.write(('%s\n' % x))
    except Exception as e:
        display.error(("Could not create retry file '%s'. The error was: %s" % (retry_path, e)))
        return False
    return True
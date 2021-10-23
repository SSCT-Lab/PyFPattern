

def sensu_subscription(module, path, name, state='present', backup=False):
    changed = False
    reasons = []
    try:
        import json
    except ImportError:
        import simplejson as json
    try:
        config = json.load(open(path))
    except IOError:
        e = get_exception()
        if (e.errno is 2):
            if (state == 'absent'):
                reasons.append("file did not exist and state is `absent'")
                return (changed, reasons)
            config = {
                
            }
        else:
            module.fail_json(msg=str(e))
    except ValueError:
        msg = '{path} contains invalid JSON'.format(path=path)
        module.fail_json(msg=msg)
    if ('client' not in config):
        if (state == 'absent'):
            reasons.append("`client' did not exist and state is `absent'")
            return (changed, reasons)
        config['client'] = {
            
        }
        changed = True
        reasons.append("`client' did not exist")
    if ('subscriptions' not in config['client']):
        if (state == 'absent'):
            reasons.append("`client.subscriptions' did not exist and state is `absent'")
            return (changed, reasons)
        config['client']['subscriptions'] = []
        changed = True
        reasons.append("`client.subscriptions' did not exist")
    if (name not in config['client']['subscriptions']):
        if (state == 'absent'):
            reasons.append('channel subscription was absent')
            return (changed, reasons)
        config['client']['subscriptions'].append(name)
        changed = True
        reasons.append("channel subscription was absent and state is `present'")
    elif (state == 'absent'):
        config['client']['subscriptions'].remove(name)
        changed = True
        reasons.append("channel subscription was present and state is `absent'")
    if (changed and (not module.check_mode)):
        if backup:
            module.backup_local(path)
        try:
            open(path, 'w').write((json.dumps(config, indent=2) + '\n'))
        except IOError:
            e = get_exception()
            module.fail_json(msg=('Failed to write to file %s: %s' % (path, str(e))))
    return (changed, reasons)

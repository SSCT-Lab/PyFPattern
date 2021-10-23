

def run(module, device_operations, connection, candidate, running, rollback_id):
    result = {
        
    }
    resp = {
        
    }
    config_diff = []
    banner_diff = {
        
    }
    replace = module.params['replace']
    commit_comment = module.params['commit_comment']
    multiline_delimiter = module.params['multiline_delimiter']
    diff_replace = module.params['diff_replace']
    diff_match = module.params['diff_match']
    diff_ignore_lines = module.params['diff_ignore_lines']
    commit = (not module.check_mode)
    if (replace in ('yes', 'true', 'True')):
        replace = True
    elif (replace in ('no', 'false', 'False')):
        replace = False
    if (rollback_id is not None):
        resp = connection.rollback(rollback_id, commit)
        if ('diff' in resp):
            result['changed'] = True
    elif device_operations.get('supports_onbox_diff'):
        if diff_replace:
            module.warn('diff_replace is ignored as the device supports onbox diff')
        if diff_match:
            module.warn('diff_mattch is ignored as the device supports onbox diff')
        if diff_ignore_lines:
            module.warn('diff_ignore_lines is ignored as the device supports onbox diff')
        if (not isinstance(candidate, list)):
            candidate = candidate.strip('\n').splitlines()
        kwargs = {
            'candidate': candidate,
            'commit': commit,
            'replace': replace,
            'comment': commit_comment,
        }
        resp = connection.edit_config(**kwargs)
        if ('diff' in resp):
            result['changed'] = True
    elif device_operations.get('supports_generate_diff'):
        kwargs = {
            'candidate': candidate,
            'running': running,
        }
        if diff_match:
            kwargs.update({
                'diff_match': diff_match,
            })
        if diff_replace:
            kwargs.update({
                'diff_replace': diff_replace,
            })
        if diff_ignore_lines:
            kwargs.update({
                'diff_ignore_lines': diff_ignore_lines,
            })
        diff_response = connection.get_diff(**kwargs)
        config_diff = diff_response.get('config_diff')
        banner_diff = diff_response.get('banner_diff')
        if config_diff:
            if isinstance(config_diff, list):
                candidate = config_diff
            else:
                candidate = config_diff.splitlines()
            kwargs = {
                'candidate': candidate,
                'commit': commit,
                'replace': replace,
                'comment': commit_comment,
            }
            if commit:
                connection.edit_config(**kwargs)
            result['changed'] = True
        if banner_diff:
            candidate = json.dumps(banner_diff)
            kwargs = {
                'candidate': candidate,
                'commit': commit,
            }
            if multiline_delimiter:
                kwargs.update({
                    'multiline_delimiter': multiline_delimiter,
                })
            if commit:
                connection.edit_banner(**kwargs)
            result['changed'] = True
    if module._diff:
        if ('diff' in resp):
            result['diff'] = {
                'prepared': resp['diff'],
            }
        else:
            diff = ''
            if config_diff:
                if isinstance(config_diff, list):
                    diff += '\n'.join(config_diff)
                else:
                    diff += config_diff
            if banner_diff:
                diff += json.dumps(banner_diff)
            result['diff'] = {
                'prepared': diff,
            }
    return result

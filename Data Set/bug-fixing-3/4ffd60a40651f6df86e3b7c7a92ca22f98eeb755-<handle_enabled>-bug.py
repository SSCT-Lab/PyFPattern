def handle_enabled(module, result, service_path):
    'Enable or disable a service as needed.\n\n    - \'preset\' will set the enabled state according to available preset file settings.\n    - \'enabled\' will set the enabled state explicitly, independently of preset settings.\n\n    These options are set to "mutually exclusive" but the explicit \'enabled\' option will\n    have priority if the check is bypassed.\n    '
    enabled = service_is_enabled(module, service_path)
    if module.params['preset']:
        action = 'preset'
        preset = (enabled is service_is_preset_enabled(module, service_path))
        result['preset'] = preset
        result['enabled'] = enabled
        if (preset != module.params['preset']):
            result['changed'] = True
            if (not module.check_mode):
                (rc, out, err) = run_sys_ctl(module, [action, service_path])
                if (rc != 0):
                    module.fail_json(msg=('Unable to %s service %s: %s' % (action, service_path, (out + err))))
            result['preset'] = (not preset)
            result['enabled'] = (not enabled)
    if (module.params['enabled'] is not None):
        if module.params['enabled']:
            action = 'enable'
        else:
            action = 'disable'
        result['enabled'] = enabled
        if (enabled != module.params['enabled']):
            result['changed'] = True
            if (not module.check_mode):
                (rc, out, err) = run_sys_ctl(module, [action, service_path])
                if (rc != 0):
                    module.fail_json(msg=('Unable to %s service %s: %s' % (action, service_path, (out + err))))
            result['enabled'] = (not enabled)
def main():
    module = AnsibleModule(argument_spec=dict(server=dict(required=True), port=dict(default='443', type='int'), user=dict(default='admin'), passwd=dict(default='admin', no_log=True)))
    if (not HAS_AOS_PYEZ):
        module.fail_json(msg='aos-pyez is not installed.  Please see details here: https://github.com/Apstra/aos-pyez')
    check_aos_version(module, '0.6.1')
    aos_login(module)
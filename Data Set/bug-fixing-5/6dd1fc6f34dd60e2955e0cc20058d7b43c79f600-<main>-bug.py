def main():
    module = AnsibleModule(argument_spec=dict(server=dict(required=True), port=dict(default='8888'), user=dict(default='admin'), passwd=dict(default='admin', no_log=True)))
    if (not HAS_AOS_PYEZ):
        module.fail_json(msg='aos-pyez is not installed.  Please see details here: https://github.com/Apstra/aos-pyez')
    aos_login(module)
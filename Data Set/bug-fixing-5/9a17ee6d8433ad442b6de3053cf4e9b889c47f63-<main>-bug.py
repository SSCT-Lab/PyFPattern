def main():
    spec = ArgumentSpec()
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)
    if (not HAS_F5SDK):
        module.fail_json(msg='The python f5-sdk module is required')
    if (not HAS_NETADDR):
        module.fail_json(msg='The python netaddr module is required')
    try:
        client = F5Client(**module.params)
        mm = ModuleManager(module=module, client=client)
        results = mm.exec_module()
        cleanup_tokens(client)
        module.exit_json(**results)
    except F5ModuleError as ex:
        cleanup_tokens(client)
        module.fail_json(msg=str(ex))
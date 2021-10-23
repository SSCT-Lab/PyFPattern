def main():
    spec = ArgumentSpec()
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)
    if (is_cli(module) and (not HAS_F5SDK)):
        module.fail_json(msg='The python f5-sdk module is required to use the REST api')
    client = F5Client(**module.params)
    try:
        mm = ModuleManager(module=module, client=client)
        results = mm.exec_module()
        if (not is_cli(module)):
            cleanup_tokens(client)
        module.exit_json(**results)
    except F5ModuleError as e:
        if (not is_cli(module)):
            cleanup_tokens(client)
        module.fail_json(msg=str(e))
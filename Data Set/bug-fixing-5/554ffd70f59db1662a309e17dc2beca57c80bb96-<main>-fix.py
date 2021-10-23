def main():
    spec = ArgumentSpec()
    client = AnsibleF5Client(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode, f5_product_name=spec.f5_product_name, mutually_exclusive=spec.mutually_exclusive)
    try:
        if (not HAS_F5SDK):
            raise F5ModuleError('The python f5-sdk module is required')
        mm = ModuleManager(client)
        results = mm.exec_module()
        cleanup_tokens(client)
        client.module.exit_json(**results)
    except F5ModuleError as e:
        cleanup_tokens(client)
        client.module.fail_json(msg=str(e))
def main():
    if (not HAS_F5SDK):
        raise F5ModuleError('The python f5-sdk module is required')
    spec = ArgumentSpec()
    client = AnsibleF5Client(argument_spec=spec.argument_spec, mutually_exclusive=spec.mutually_exclusive, supports_check_mode=spec.supports_check_mode, f5_product_name=spec.f5_product_name)
    try:
        mm = ModuleManager(client)
        results = mm.exec_module()
        client.module.exit_json(**results)
    except F5ModuleError as e:
        client.module.fail_json(msg=str(e))
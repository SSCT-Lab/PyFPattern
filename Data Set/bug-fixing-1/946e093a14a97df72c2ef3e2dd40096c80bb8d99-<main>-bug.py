

def main():
    spec = ArgumentSpec()
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)
    try:
        client = F5RestClient(**module.params)
        mm = ModuleManager(module=module, client=client)
        results = mm.exec_module()
        cleanup_tokens(client)
        exit_json(module, results, client)
    except F5ModuleError as ex:
        cleanup_tokens(client)
        fail_json(module, ex, client)



def apply_patch(module, commands):
    for command in commands:
        load_config(module, [command])
        time.sleep(5)
        if ('failed' in response):
            module.fail_json(msg='Operation failed!', response=response)

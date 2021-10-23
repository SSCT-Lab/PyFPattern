def apply_patch(module, commands):
    for command in commands:
        load_config(module, [command])
        time.sleep(5)
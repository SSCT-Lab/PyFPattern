

def get_all_image_info(module, executable):
    command = [executable, 'image', 'ls', '-q']
    (rc, out, err) = module.run_command(command)
    name = out.split('\n')
    out = get_image_info(module, executable, name)
    return out

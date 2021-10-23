def get_name(module, pacman_output, from_sync=False):
    'Take pacman -Qi or pacman -Si output and get the package name'
    lines = pacman_output.split('\n')
    index = 0
    if from_sync:
        index = 1
    try:
        name = lines[index].split(':')[1].strip()
    except IndexError:
        module.fail_json(msg='get_name: fail to retrieve package name from pacman output')
    return name
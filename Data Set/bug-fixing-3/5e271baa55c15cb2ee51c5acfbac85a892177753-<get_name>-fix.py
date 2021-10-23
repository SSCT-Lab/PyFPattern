def get_name(module, pacman_output):
    'Take pacman -Qi or pacman -Si output and get the package name'
    lines = pacman_output.split('\n')
    for line in lines:
        if line.startswith('Name '):
            return line.split(':')[1].strip()
    module.fail_json(msg='get_name: fail to retrieve package name from pacman output')
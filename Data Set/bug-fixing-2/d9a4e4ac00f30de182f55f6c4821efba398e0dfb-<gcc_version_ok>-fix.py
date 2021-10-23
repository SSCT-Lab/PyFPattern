

def gcc_version_ok(self, min_gcc_major_version, min_gcc_minor_version):
    'Make sure the GCC version installed on the machine is acceptable.'
    gcc_path = ''
    gcc_path_cmd = 'command -v gcc'
    try:
        print('gcc_path_cmd = {}'.format(gcc_path_cmd))
        gcc_path = subprocess.check_output(gcc_path_cmd, shell=True, stderr=subprocess.STDOUT).strip()
        print('gcc located here: {}'.format(gcc_path))
        if (not os.access(gcc_path, (os.F_OK | os.X_OK))):
            raise ValueError('{} does not exist or is not executable.'.format(gcc_path))
        gcc_output = subprocess.check_output([gcc_path, '-dumpfullversion', '-dumpversion'], stderr=subprocess.STDOUT).strip()
        if isinstance(gcc_output, bytes):
            gcc_output = gcc_output.decode('utf-8')
        print('gcc version: {}'.format(gcc_output))
        gcc_info = gcc_output.split('.')
        if (gcc_info[0] < min_gcc_major_version):
            print('Your MAJOR version of GCC is too old: {}; it must be at least {}.{}'.format(gcc_info[0], min_gcc_major_version, min_gcc_minor_version))
            return False
        elif (gcc_info[0] == min_gcc_major_version):
            if (gcc_info[1] < min_gcc_minor_version):
                print('Your MINOR version of GCC is too old: {}; it must be at least {}.{}'.format(gcc_info[1], min_gcc_major_version, min_gcc_minor_version))
                return False
            return True
        else:
            self._debug('gcc version OK: {}.{}'.format(gcc_info[0], gcc_info[1]))
            return True
    except subprocess.CalledProcessException as e:
        print('Problem getting gcc info: {}'.format(e))
        return False

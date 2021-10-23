

def check_compiler_abi_compatibility(compiler):
    '\n    Verifies that the given compiler is ABI-compatible with PyTorch.\n\n    Arguments:\n        compiler (str): The compiler executable name to check (e.g. ``g++``).\n            Must be executable in a shell process.\n\n    Returns:\n        False if the compiler is (likely) ABI-incompatible with PyTorch,\n        else True.\n    '
    try:
        check_cmd = ('{}' if (sys.platform == 'win32') else '{} --version')
        info = subprocess.check_output(check_cmd.format(compiler).split(), stderr=subprocess.STDOUT)
    except Exception:
        (_, error, _) = sys.exc_info()
        warnings.warn('Error checking compiler version: {}'.format(error))
    else:
        info = info.decode().lower()
        if (('gcc' in info) or ('g++' in info)):
            version = re.search('(\\d+)\\.(\\d+|x)', info)
            if (version is not None):
                (major, minor) = version.groups()
                minor = (0 if (minor == 'x') else int(minor))
                if ((int(major), minor) >= MINIMUM_GCC_VERSION):
                    return True
                else:
                    compiler = '{} {}'.format(compiler, version.group(0))
        elif ('Microsoft' in info):
            info = info.decode().lower()
            version = re.search('(\\d+)\\.(\\d+)\\.(\\d+)', info)
            if (version is not None):
                (major, minor, revision) = version.groups()
                if ((int(major), int(minor), int(revision)) >= MINIMUM_MSVC_VERSION):
                    return True
                else:
                    compiler = '{} {}'.format(compiler, version.group(0))
    warnings.warn(ABI_INCOMPATIBILITY_WARNING.format(compiler))
    return False

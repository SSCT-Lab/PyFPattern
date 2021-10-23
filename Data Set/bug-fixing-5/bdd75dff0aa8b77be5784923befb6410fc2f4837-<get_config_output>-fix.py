def get_config_output(self, config_exe, option):
    cmd = ((((config_exe + ' ') + self.append_config_exe) + ' ') + option)
    try:
        o = subprocess.check_output(cmd)
    except (OSError, subprocess.CalledProcessError):
        pass
    else:
        o = filepath_from_subprocess_output(o)
        return o
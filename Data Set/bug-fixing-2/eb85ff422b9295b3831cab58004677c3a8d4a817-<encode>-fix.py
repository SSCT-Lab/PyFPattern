

def encode(self, command, source, dest, pretend=False):
    'Encode `source` to `dest` using command template `command`.\n\n        Raises `subprocess.CalledProcessError` if the command exited with a\n        non-zero status code.\n        '
    assert isinstance(command, bytes)
    assert isinstance(source, bytes)
    assert isinstance(dest, bytes)
    quiet = self.config['quiet'].get(bool)
    if ((not quiet) and (not pretend)):
        self._log.info('Encoding {0}', util.displayable_path(source))
    if (not six.PY2):
        command = command.decode(util.arg_encoding(), 'surrogateescape')
        source = source.decode(util.arg_encoding(), 'surrogateescape')
        dest = dest.decode(util.arg_encoding(), 'surrogateescape')
    args = shlex.split(command)
    encode_cmd = []
    for (i, arg) in enumerate(args):
        args[i] = Template(arg).safe_substitute({
            'source': source,
            'dest': dest,
        })
        if six.PY2:
            encode_cmd.append(args[i])
        else:
            encode_cmd.append(args[i].encode(util.arg_encoding()))
    if pretend:
        self._log.info('{0}', ' '.join(ui.decargs(args)))
        return
    try:
        util.command_output(encode_cmd)
    except subprocess.CalledProcessError as exc:
        self._log.info('Encoding {0} failed. Cleaning up...', util.displayable_path(source))
        self._log.debug('Command {0} exited with status {1}: {2}', args, exc.returncode, exc.output)
        util.remove(dest)
        util.prune_dirs(os.path.dirname(dest))
        raise
    except OSError as exc:
        raise ui.UserError("convert: couldn't invoke '{0}': {1}".format(' '.join(ui.decargs(args)), exc))
    if ((not quiet) and (not pretend)):
        self._log.info('Finished encoding {0}', util.displayable_path(source))

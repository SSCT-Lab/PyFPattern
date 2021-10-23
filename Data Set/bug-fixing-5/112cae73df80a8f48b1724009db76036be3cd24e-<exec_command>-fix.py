def exec_command(module, command):
    try:
        sf = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sf.connect(module._socket_path)
        data = ('EXEC: %s' % command)
        send_data(sf, to_bytes(data.strip()))
        rc = int(recv_data(sf), 10)
        stdout = recv_data(sf)
        stderr = recv_data(sf)
    except socket.error:
        exc = get_exception()
        sf.close()
        module.fail_json(msg='unable to connect to socket', err=str(exc))
    sf.close()
    return (rc, to_native(stdout, errors='surrogate_or_strict'), to_native(stderr, errors='surrogate_or_strict'))
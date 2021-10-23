def input_loop(chan, using_pty):
    while (not chan.exit_status_ready()):
        if win32:
            have_char = msvcrt.kbhit()
        else:
            (r, w, x) = select([sys.stdin], [], [], 0.0)
            have_char = (r and (r[0] == sys.stdin))
        if (have_char and chan.input_enabled):
            byte = (msvcrt.getch() if win32 else os.read(sys.stdin.fileno(), 1))
            chan.sendall(byte)
            if ((not using_pty) and env.echo_stdin):
                sys.stdout.write(byte)
                sys.stdout.flush()
        time.sleep(ssh.io_sleep)
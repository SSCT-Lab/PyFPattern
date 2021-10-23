def run(self):
    try:
        while (not self.connection._conn_closed):
            signal.signal(signal.SIGALRM, self.connect_timeout)
            signal.signal(signal.SIGTERM, self.handler)
            signal.alarm(self.connection.get_option('persistent_connect_timeout'))
            self.exception = None
            (s, addr) = self.sock.accept()
            signal.alarm(0)
            signal.signal(signal.SIGALRM, self.command_timeout)
            while True:
                data = recv_data(s)
                if (not data):
                    break
                log_messages = self.connection.get_option('persistent_log_messages')
                if log_messages:
                    display.display(('jsonrpc request: %s' % data), log_only=True)
                signal.alarm(self.connection.get_option('persistent_command_timeout'))
                resp = self.srv.handle_request(data)
                signal.alarm(0)
                if log_messages:
                    display.display(('jsonrpc response: %s' % resp), log_only=True)
                send_data(s, to_bytes(resp))
            s.close()
    except Exception as e:
        if hasattr(e, 'errno'):
            if (e.errno != errno.EINTR):
                self.exception = traceback.format_exc()
        else:
            self.exception = traceback.format_exc()
    finally:
        time.sleep(0.1)
        self.shutdown()
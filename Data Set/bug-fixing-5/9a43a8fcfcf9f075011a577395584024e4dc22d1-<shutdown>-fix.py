def shutdown(self):
    ' Shuts down the local domain socket\n        '
    lock_path = unfrackpath(('%s/.ansible_pc_lock_%s' % os.path.split(self.socket_path)))
    if os.path.exists(self.socket_path):
        try:
            if self.sock:
                self.sock.close()
            if self.connection:
                self.connection.close()
                if self.connection.get_option('persistent_log_messages'):
                    for (_level, message) in self.connection.pop_messages():
                        display.display(message, log_only=True)
        except Exception:
            pass
        finally:
            if os.path.exists(self.socket_path):
                os.remove(self.socket_path)
                setattr(self.connection, '_socket_path', None)
                setattr(self.connection, '_connected', False)
    if os.path.exists(lock_path):
        os.remove(lock_path)
    display.display('shutdown complete', log_only=True)
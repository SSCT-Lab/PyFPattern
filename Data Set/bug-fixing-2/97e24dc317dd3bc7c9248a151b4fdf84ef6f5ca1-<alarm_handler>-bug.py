

def alarm_handler(self, signum, frame):
    'Alarm handler raised in case of command timeout '
    display.display('closing shell due to sigalarm', log_only=True)
    self.close_shell()

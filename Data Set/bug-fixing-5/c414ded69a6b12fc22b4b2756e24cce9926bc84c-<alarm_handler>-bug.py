def alarm_handler(self, signum, frame):
    'Alarm handler raised in case of command timeout '
    self.close_shell()
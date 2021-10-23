def _read_task_logs(self, stream):
    while True:
        line = stream.readline().decode('utf-8')
        if (len(line) == 0):
            break
        self.logger.info('Subtask: {}'.format(line.rstrip('\n')))
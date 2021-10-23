def process_state(self):
    '\n        Function to manage state\n        '
    if (self.state == 'present'):
        self.add_portgroup()
    elif (self.state == 'absent'):
        self.remove_portgroup()
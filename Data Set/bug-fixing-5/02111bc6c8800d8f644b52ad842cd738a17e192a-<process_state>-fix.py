def process_state(self):
    '\n        Function to manage state\n        '
    if (self.state == 'present'):
        self.add_hosts_port_group()
    elif (self.state == 'absent'):
        self.remove_hosts_port_group()
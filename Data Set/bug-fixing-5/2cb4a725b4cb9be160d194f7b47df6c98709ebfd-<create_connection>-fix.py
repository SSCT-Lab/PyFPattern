def create_connection(self):
    cmd = []
    if (self.type == 'team'):
        if ((self.dns4 is not None) or (self.dns6 is not None)):
            cmd = self.create_connection_team()
            self.execute_command(cmd)
            cmd = self.modify_connection_team()
            self.execute_command(cmd)
            cmd = self.up_connection()
        elif ((self.dns4 is None) or (self.dns6 is None)):
            cmd = self.create_connection_team()
    elif (self.type == 'team-slave'):
        if (self.mtu is not None):
            cmd = self.create_connection_team_slave()
            self.execute_command(cmd)
            cmd = self.modify_connection_team_slave()
            self.execute_command(cmd)
        else:
            cmd = self.create_connection_team_slave()
    elif (self.type == 'bond'):
        if ((self.mtu is not None) or (self.dns4 is not None) or (self.dns6 is not None)):
            cmd = self.create_connection_bond()
            self.execute_command(cmd)
            cmd = self.modify_connection_bond()
            self.execute_command(cmd)
            cmd = self.up_connection()
        else:
            cmd = self.create_connection_bond()
    elif (self.type == 'bond-slave'):
        cmd = self.create_connection_bond_slave()
    elif (self.type == 'ethernet'):
        if ((self.mtu is not None) or (self.dns4 is not None) or (self.dns6 is not None)):
            cmd = self.create_connection_ethernet()
            self.execute_command(cmd)
            cmd = self.modify_connection_ethernet()
            self.execute_command(cmd)
            cmd = self.up_connection()
        else:
            cmd = self.create_connection_ethernet()
    elif (self.type == 'bridge'):
        cmd = self.create_connection_bridge()
    elif (self.type == 'vlan'):
        cmd = self.create_connection_vlan()
    if cmd:
        return self.execute_command(cmd)
    else:
        self.module.fail_json(msg="Type of device or network connection is required while performing 'create' operation. Please specify 'type' as an argument.")
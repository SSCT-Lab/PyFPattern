def modify_connection(self):
    cmd = []
    if (self.type == 'team'):
        cmd = self.modify_connection_team()
    elif (self.type == 'team-slave'):
        cmd = self.modify_connection_team_slave()
    elif (self.type == 'bond'):
        cmd = self.modify_connection_bond()
    elif (self.type == 'bond-slave'):
        cmd = self.modify_connection_bond_slave()
    elif (self.type == 'ethernet'):
        cmd = self.modify_connection_ethernet()
    elif (self.type == 'bridge'):
        cmd = self.modify_connection_bridge()
    elif (self.type == 'vlan'):
        cmd = self.modify_connection_vlan()
    return self.execute_command(cmd)
def populate_interfaces(self, lines1, lines2):
    interfaces = dict()
    for (line1, line2) in zip(lines1, lines2):
        line = ((line1 + '  ') + line2)
        intfSplit = line.split()
        innerData = dict()
        innerData['description'] = intfSplit[6].strip()
        innerData['macaddress'] = intfSplit[8].strip()
        innerData['mtu'] = intfSplit[9].strip()
        innerData['speed'] = intfSplit[1].strip()
        innerData['duplex'] = intfSplit[2].strip()
        innerData['operstatus'] = intfSplit[5].strip()
        interfaces[intfSplit[0].strip()] = innerData
    return interfaces
def semanage_port_get_type(seport, port, proto):
    ' Get the SELinux type of the specified port.\n\n    :param seport: Instance of seobject.portRecords\n\n    :type port: str\n    :param port: Port or port range (example: "8080", "8080-9090")\n\n    :type proto: str\n    :param proto: Protocol (\'tcp\' or \'udp\')\n\n    :rtype: tuple\n    :return: Tuple containing the SELinux type and MLS/MCS level, or None if not found.\n    '
    ports = port.split('-', 1)
    if (len(ports) == 1):
        ports.extend(ports)
    key = (int(ports[0]), int(ports[1]), proto)
    records = seport.get_all()
    if (key in records):
        return records[key]
    else:
        return None
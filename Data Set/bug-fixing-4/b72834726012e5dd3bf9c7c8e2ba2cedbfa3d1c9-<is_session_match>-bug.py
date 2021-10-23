def is_session_match(self):
    'is bfd session match'
    if ((not self.bfd_dict['session']) or (not self.session_name)):
        return False
    session = self.bfd_dict['session']
    if (self.session_name != session.get('sessName', '')):
        return False
    if (self.create_type and (self.create_type.upper() not in session.get('createType', '').upper())):
        return False
    if (self.addr_type and (self.addr_type != session.get('addrType').lower())):
        return False
    if (self.dest_addr and (self.dest_addr != session.get('destAddr'))):
        return False
    if (self.src_addr and (self.src_addr != session.get('srcAddr'))):
        return False
    if self.out_if_name:
        if (not session.get('outIfName')):
            return False
        if (self.out_if_name.replace(' ', '').lower() != session.get('outIfName').replace(' ', '').lower()):
            return False
    if (self.vrf_name and (self.vrf_name != session.get('vrfName'))):
        return False
    if (str(self.use_default_ip).lower() != session.get('useDefaultIp')):
        return False
    return True
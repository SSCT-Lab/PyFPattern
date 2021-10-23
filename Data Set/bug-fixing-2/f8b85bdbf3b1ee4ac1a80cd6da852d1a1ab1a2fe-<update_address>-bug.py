

def update_address(self, attachments_service, attachment, network):
    for ip in attachment.ip_address_assignments:
        if (str(ip.ip.version) == network.get('version', 'v4')):
            changed = False
            if (not equal(network.get('boot_protocol'), str(ip.assignment_method))):
                ip.assignment_method = otypes.BootProtocol(network.get('boot_protocol'))
                changed = True
            if (not equal(network.get('address'), ip.ip.address)):
                ip.ip.address = network.get('address')
                changed = True
            if (not equal(network.get('gateway'), ip.ip.gateway)):
                ip.ip.gateway = network.get('gateway')
                changed = True
            if (not equal(network.get('prefix'), (int(ip.ip.netmask) if ip.ip.netmask else None))):
                ip.ip.netmask = str(network.get('prefix'))
                changed = True
            if changed:
                if (not self._module.check_mode):
                    attachments_service.service(attachment.id).update(attachment)
                self.changed = True
                break

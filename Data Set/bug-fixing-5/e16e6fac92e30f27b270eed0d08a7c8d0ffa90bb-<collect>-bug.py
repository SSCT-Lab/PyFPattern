def collect(self, module=None, collected_facts=None):
    ssh_pub_key_facts = {
        
    }
    keytypes = ('dsa', 'rsa', 'ecdsa', 'ed25519')
    keydirs = ['/etc/ssh', '/etc/openssh', '/etc']
    for keydir in keydirs:
        for type_ in keytypes:
            factname = ('ssh_host_key_%s_public' % type_)
            if (factname in ssh_pub_key_facts):
                return ssh_pub_key_facts
            key_filename = ('%s/ssh_host_%s_key.pub' % (keydir, type_))
            keydata = get_file_content(key_filename)
            if (keydata is not None):
                ssh_pub_key_facts[factname] = keydata.split()[1]
    return ssh_pub_key_facts
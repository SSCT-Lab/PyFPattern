

def collect(self, module=None, collected_facts=None):
    ssh_pub_key_facts = {
        
    }
    algos = ('dsa', 'rsa', 'ecdsa', 'ed25519')
    keydirs = ['/etc/ssh', '/etc/openssh', '/etc']
    for keydir in keydirs:
        for algo in algos:
            factname = ('ssh_host_key_%s_public' % algo)
            if (factname in ssh_pub_key_facts):
                return ssh_pub_key_facts
            key_filename = ('%s/ssh_host_%s_key.pub' % (keydir, algo))
            keydata = get_file_content(key_filename)
            if (keydata is not None):
                (keytype, key) = keydata.split()[0:2]
                ssh_pub_key_facts[factname] = key
                ssh_pub_key_facts[(factname + '_keytype')] = keytype
    return ssh_pub_key_facts

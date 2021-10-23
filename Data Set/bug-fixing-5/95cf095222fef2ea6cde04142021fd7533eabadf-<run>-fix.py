def run(self, terms, variables, **kwargs):
    vault_args = terms[0].split(' ')
    vault_dict = {
        
    }
    ret = []
    for param in vault_args:
        try:
            (key, value) = param.split('=')
        except ValueError as e:
            raise AnsibleError(('hashi_vault plugin needs key=value pairs, but received %s' % terms))
        vault_dict[key] = value
    vault_conn = HashiVault(**vault_dict)
    for term in terms:
        key = term.split()[0]
        value = vault_conn.get()
        ret.append(value)
    return ret
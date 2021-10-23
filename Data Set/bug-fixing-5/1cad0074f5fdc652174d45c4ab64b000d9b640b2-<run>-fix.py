def run(self, terms, variables, **kwargs):
    if (not HAS_HVAC):
        raise AnsibleError('Please pip install hvac to use the hashi_vault lookup module.')
    vault_args = terms[0].split(' ')
    vault_dict = {
        
    }
    ret = []
    for param in vault_args:
        try:
            (key, value) = param.split('=')
        except ValueError:
            raise AnsibleError(('hashi_vault lookup plugin needs key=value pairs, but received %s' % terms))
        vault_dict[key] = value
    vault_conn = HashiVault(**vault_dict)
    for term in terms:
        key = term.split()[0]
        value = vault_conn.get()
        ret.append(value)
    return ret
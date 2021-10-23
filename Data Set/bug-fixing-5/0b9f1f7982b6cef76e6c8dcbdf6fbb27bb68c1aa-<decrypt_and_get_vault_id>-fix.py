def decrypt_and_get_vault_id(self, vaulttext, filename=None):
    'Decrypt a piece of vault encrypted data.\n\n        :arg vaulttext: a string to decrypt.  Since vault encrypted data is an\n            ascii text format this can be either a byte str or unicode string.\n        :kwarg filename: a filename that the data came from.  This is only\n            used to make better error messages in case the data cannot be\n            decrypted.\n        :returns: a byte string containing the decrypted data and the vault-id that was used\n\n        '
    b_vaulttext = to_bytes(vaulttext, errors='strict', encoding='utf-8')
    if (self.secrets is None):
        raise AnsibleVaultError('A vault password must be specified to decrypt data')
    if (not is_encrypted(b_vaulttext)):
        msg = 'input is not vault encrypted data'
        if filename:
            msg += ('%s is not a vault encrypted file' % to_native(filename))
        raise AnsibleError(msg)
    (b_vaulttext, dummy, cipher_name, vault_id) = parse_vaulttext_envelope(b_vaulttext, filename=filename)
    if (cipher_name in CIPHER_WHITELIST):
        this_cipher = CIPHER_MAPPING[cipher_name]()
    else:
        raise AnsibleError('{0} cipher could not be found'.format(cipher_name))
    b_plaintext = None
    if (not self.secrets):
        raise AnsibleVaultError('Attempting to decrypt but no vault secrets found')
    vault_id_matchers = []
    vault_id_used = None
    if vault_id:
        display.vvvvv(('Found a vault_id (%s) in the vaulttext' % vault_id))
        vault_id_matchers.append(vault_id)
        _matches = match_secrets(self.secrets, vault_id_matchers)
        if _matches:
            display.vvvvv(('We have a secret associated with vault id (%s), will try to use to decrypt %s' % (vault_id, to_text(filename))))
        else:
            display.vvvvv(('Found a vault_id (%s) in the vault text, but we do not have a associated secret (--vault-id)' % vault_id))
    if (not C.DEFAULT_VAULT_ID_MATCH):
        vault_id_matchers.extend([_vault_id for (_vault_id, _dummy) in self.secrets if (_vault_id != vault_id)])
    matched_secrets = match_secrets(self.secrets, vault_id_matchers)
    for (vault_secret_id, vault_secret) in matched_secrets:
        display.vvvvv(('Trying to use vault secret=(%s) id=%s to decrypt %s' % (vault_secret, vault_secret_id, to_text(filename))))
        try:
            display.vvvv(('Trying secret %s for vault_id=%s' % (vault_secret, vault_secret_id)))
            b_plaintext = this_cipher.decrypt(b_vaulttext, vault_secret)
            if (b_plaintext is not None):
                vault_id_used = vault_secret_id
                display.vvvvv(('decrypt succesful with secret=%s and vault_id=%s' % (vault_secret, vault_secret_id)))
                break
        except AnsibleVaultFormatError as exc:
            msg = 'There was a vault format error'
            if filename:
                msg += (' in %s' % to_text(filename))
            msg += (': %s' % exc)
            display.warning(msg)
            raise
        except AnsibleError as e:
            display.vvvv(('Tried to use the vault secret (%s) to decrypt (%s) but it failed. Error: %s' % (vault_secret_id, to_text(filename), e)))
            continue
    else:
        msg = 'Decryption failed (no vault secrets were found that could decrypt)'
        if filename:
            msg += (' on %s' % to_native(filename))
        raise AnsibleVaultError(msg)
    if (b_plaintext is None):
        msg = 'Decryption failed'
        if filename:
            msg += (' on %s' % to_native(filename))
        raise AnsibleError(msg)
    return (b_plaintext, vault_id_used)
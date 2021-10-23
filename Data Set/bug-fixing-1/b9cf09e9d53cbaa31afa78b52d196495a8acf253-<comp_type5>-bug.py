

def comp_type5(unencrypted_password, encrypted_password, return_orginal=False):
    salt = hash_salt(encrypted_password)
    if (type5_pw(unencrypted_password, salt) == encrypted_password):
        if (return_orginal is True):
            return encrypted_password
        else:
            return True
    return False

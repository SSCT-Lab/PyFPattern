def get_verification_attributes(connection, module, identity):
    response = call_and_handle_errors(module, connection.get_identity_verification_attributes, Identities=[identity])
    identity_verification = response['VerificationAttributes']
    if (identity not in identity_verification):
        return None
    return identity_verification[identity]
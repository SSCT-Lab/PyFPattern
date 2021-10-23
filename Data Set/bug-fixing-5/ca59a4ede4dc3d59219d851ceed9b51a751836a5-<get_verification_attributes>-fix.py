def get_verification_attributes(connection, module, identity, retries=0, retryDelay=10):
    for attempt in range(0, (retries + 1)):
        response = call_and_handle_errors(module, connection.get_identity_verification_attributes, Identities=[identity])
        identity_verification = response['VerificationAttributes']
        if (identity in identity_verification):
            break
        time.sleep(retryDelay)
    if (identity not in identity_verification):
        return None
    return identity_verification[identity]
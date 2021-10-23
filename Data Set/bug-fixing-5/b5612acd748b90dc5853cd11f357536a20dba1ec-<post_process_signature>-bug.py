def post_process_signature(signature):
    parts = signature.split('.')
    if (len(parts) >= 4):
        if (parts[1] == 'layers'):
            signature = ('keras.layers.' + '.'.join(parts[3:]))
        if (parts[1] == 'utils'):
            signature = ('keras.utils.' + '.'.join(parts[3:]))
        if (parts[1] == 'backend'):
            signature = ('keras.backend.' + '.'.join(parts[3:]))
    return signature
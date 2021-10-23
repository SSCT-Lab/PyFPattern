

def convert_key_to_base64(module):
    ' IOS-XR only accepts base64 decoded files, this converts the public key to a temp file.\n    '
    if module.params['aggregate']:
        name = 'aggregate'
    else:
        name = module.params['name']
    if module.params['public_key_contents']:
        key = module.params['public_key_contents']
    elif module.params['public_key']:
        readfile = open(module.params['public_key'], 'r')
        key = readfile.read()
    splitfile = key.split()[1]
    base64key = b64decode(splitfile)
    base64file = open(('/tmp/publickey_%s.b64' % name), 'wb')
    base64file.write(base64key)
    base64file.close()
    return ('/tmp/publickey_%s.b64' % name)

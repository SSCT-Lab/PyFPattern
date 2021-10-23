def commit_configuration(module, confirm=False, check=False, comment=None, confirm_timeout=None):
    obj = Element('commit-configuration')
    if confirm:
        SubElement(obj, 'confirmed')
    if check:
        SubElement(obj, 'check')
    if comment:
        subele = SubElement(obj, 'log')
        subele.text = str(comment)
    if confirm_timeout:
        subele = SubElement(obj, 'confirm-timeout')
        subele.text = int(confirm_timeout)
    return send_request(module, obj)
def aci_response(result, rawoutput, rest_type='xml'):
    ' Handle APIC response output '
    if (rest_type == 'json'):
        aci_response_json(result, rawoutput)
    else:
        aci_response_xml(result, rawoutput)
    if HAS_URLPARSE:
        result['changed'] = aci_changed(result)
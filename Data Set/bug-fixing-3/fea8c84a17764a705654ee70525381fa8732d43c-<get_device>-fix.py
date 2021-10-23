def get_device(device_ip):
    'Query OneClick for the device using the IP Address'
    resource = '/models'
    landscape_min = ('0x%x' % int(module.params.get('landscape'), 16))
    landscape_max = ('0x%x' % (int(module.params.get('landscape'), 16) + 1048576))
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n        <rs:model-request throttlesize="5"\n        xmlns:rs="http://www.ca.com/spectrum/restful/schema/request"\n        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n        xsi:schemaLocation="http://www.ca.com/spectrum/restful/schema/request ../../../xsd/Request.xsd">\n            <rs:target-models>\n            <rs:models-search>\n                <rs:search-criteria xmlns="http://www.ca.com/spectrum/restful/schema/filter">\n                    <action-models>\n                        <filtered-models>\n                            <and>\n                                <equals>\n                                    <model-type>SearchManager</model-type>\n                                </equals>\n                                <greater-than>\n                                    <attribute id="0x129fa">\n                                        <value>{mh_min}</value>\n                                    </attribute>\n                                </greater-than>\n                                <less-than>\n                                    <attribute id="0x129fa">\n                                        <value>{mh_max}</value>\n                                    </attribute>\n                                </less-than>\n                            </and>\n                        </filtered-models>\n                        <action>FIND_DEV_MODELS_BY_IP</action>\n                        <attribute id="AttributeID.NETWORK_ADDRESS">\n                            <value>{search_ip}</value>\n                        </attribute>\n                    </action-models>\n                </rs:search-criteria>\n            </rs:models-search>\n            </rs:target-models>\n            <rs:requested-attribute id="0x12d7f" /> <!--Network Address-->\n        </rs:model-request>\n        '.format(search_ip=device_ip, mh_min=landscape_min, mh_max=landscape_max)
    result = post(resource, xml=xml)
    root = ET.fromstring(result)
    if (root.get('total-models') == '0'):
        return None
    namespace = dict(ca='http://www.ca.com/spectrum/restful/schema/response')
    model = root.find('ca:model-responses', namespace).find('ca:model', namespace)
    if model.get('error'):
        module.fail_json(msg=('error checking device: %s' % model.get('error')))
    model_handle = model.get('mh')
    model_address = model.find('./*[@id="0x12d7f"]').text
    model_landscape = ('0x%x' % int(((int(model_handle, 16) // 1048576) * 1048576)))
    device = dict(model_handle=model_handle, address=model_address, landscape=model_landscape)
    return device
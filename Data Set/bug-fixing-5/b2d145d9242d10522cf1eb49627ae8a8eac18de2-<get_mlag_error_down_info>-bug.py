def get_mlag_error_down_info(self):
    ' get error down info.'
    mlag_error_down_info = dict()
    conf_str = CE_NC_GET_MLAG_ERROR_DOWN_INFO
    xml_str = get_nc_config(self.module, conf_str)
    if ('<data/>' in xml_str):
        return mlag_error_down_info
    else:
        xml_str = xml_str.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
        mlag_error_down_info['mlagErrorDownInfos'] = list()
        root = ElementTree.fromstring(xml_str)
        mlag_error_infos = root.findall('data/mlag/errordowns/errordown')
        if mlag_error_infos:
            for mlag_error_info in mlag_error_infos:
                mlag_error_dict = dict()
                for ele in mlag_error_info:
                    if (ele.tag in ['dfsgroupId', 'portName']):
                        mlag_error_dict[ele.tag] = ele.text
                mlag_error_down_info['mlagErrorDownInfos'].append(mlag_error_dict)
        return mlag_error_down_info
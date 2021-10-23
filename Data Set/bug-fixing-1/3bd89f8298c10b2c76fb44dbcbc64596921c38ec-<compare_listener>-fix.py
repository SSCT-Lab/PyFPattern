

def compare_listener(current_listener, new_listener):
    '\n    Compare two listeners.\n\n    :param current_listener:\n    :param new_listener:\n    :return:\n    '
    modified_listener = {
        
    }
    if (current_listener['Port'] != new_listener['Port']):
        modified_listener['Port'] = new_listener['Port']
    if (current_listener['Protocol'] != new_listener['Protocol']):
        modified_listener['Protocol'] = new_listener['Protocol']
    if ((current_listener['Protocol'] == 'HTTPS') and (new_listener['Protocol'] == 'HTTPS')):
        if (current_listener['SslPolicy'] != new_listener['SslPolicy']):
            modified_listener['SslPolicy'] = new_listener['SslPolicy']
        if (current_listener['Certificates'][0]['CertificateArn'] != new_listener['Certificates'][0]['CertificateArn']):
            modified_listener['Certificates'] = []
            modified_listener['Certificates'].append({
                
            })
            modified_listener['Certificates'][0]['CertificateArn'] = new_listener['Certificates'][0]['CertificateArn']
    elif ((current_listener['Protocol'] != 'HTTPS') and (new_listener['Protocol'] == 'HTTPS')):
        modified_listener['SslPolicy'] = new_listener['SslPolicy']
        modified_listener['Certificates'] = []
        modified_listener['Certificates'].append({
            
        })
        modified_listener['Certificates'][0]['CertificateArn'] = new_listener['Certificates'][0]['CertificateArn']
    if (current_listener['DefaultActions'][0]['TargetGroupArn'] != new_listener['DefaultActions'][0]['TargetGroupArn']):
        modified_listener['DefaultActions'] = []
        modified_listener['DefaultActions'].append({
            
        })
        modified_listener['DefaultActions'][0]['TargetGroupArn'] = new_listener['DefaultActions'][0]['TargetGroupArn']
        modified_listener['DefaultActions'][0]['Type'] = 'forward'
    if modified_listener:
        return modified_listener
    else:
        return None

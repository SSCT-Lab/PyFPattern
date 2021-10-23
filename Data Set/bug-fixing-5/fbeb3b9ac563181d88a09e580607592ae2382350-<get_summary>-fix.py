def get_summary(results_list, reference_point):
    summary_string = results_list[(reference_point + 1)]
    summary_list = summary_string.split(',')
    summary = dict(packets_tx=int(summary_list[0].split('packets')[0].strip()), packets_rx=int(summary_list[1].split('packets')[0].strip()), packet_loss=summary_list[2].split('packet')[0].strip())
    if ('bytes from' not in results_list[(reference_point - 2)]):
        ping_pass = False
    else:
        ping_pass = True
    return (summary, ping_pass)
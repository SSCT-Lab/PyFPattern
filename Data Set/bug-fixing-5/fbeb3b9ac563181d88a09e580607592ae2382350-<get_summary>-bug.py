def get_summary(results_list, reference_point):
    summary_string = results_list[(reference_point + 1)]
    summary_list = summary_string.split(',')
    pkts_tx = summary_list[0].split('packets')[0].strip()
    pkts_rx = summary_list[1].split('packets')[0].strip()
    pkt_loss = summary_list[2].split('packet')[0].strip()
    summary = dict(packets_tx=pkts_tx, packets_rx=pkts_rx, packet_loss=pkt_loss)
    if ('bytes from' not in results_list[(reference_point - 2)]):
        ping_pass = False
    else:
        ping_pass = True
    return (summary, ping_pass)
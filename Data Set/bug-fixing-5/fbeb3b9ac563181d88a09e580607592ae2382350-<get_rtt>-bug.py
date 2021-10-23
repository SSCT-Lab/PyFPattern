def get_rtt(results_list, packet_loss, location):
    if (packet_loss != '100.00%'):
        rtt_string = results_list[location]
        base = rtt_string.split('=')[1]
        rtt_list = base.split('/')
        min_rtt = rtt_list[0].lstrip()
        avg_rtt = rtt_list[1]
        max_rtt = rtt_list[2][:(- 3)]
        rtt = dict(min=min_rtt, avg=avg_rtt, max=max_rtt)
    else:
        rtt = dict(min=None, avg=None, max=None)
    return rtt
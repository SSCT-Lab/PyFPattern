

def get_host_ip_address():
    return socket.gethostbyname(socket.getfqdn())

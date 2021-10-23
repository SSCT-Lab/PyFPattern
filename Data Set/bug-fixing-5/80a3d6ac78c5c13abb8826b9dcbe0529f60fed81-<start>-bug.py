def start(self):
    if (self.tls_ca or self.tls_key or self.tls_cert):
        from distributed.security import Security
        security = Security(tls_client_key=self.tls_key, tls_client_cert=self.tls_cert, tls_ca_file=self.tls_ca)
    else:
        security = None
    self.client = distributed.Client(self.cluster_address, security=security)
    self.futures = {
        
    }
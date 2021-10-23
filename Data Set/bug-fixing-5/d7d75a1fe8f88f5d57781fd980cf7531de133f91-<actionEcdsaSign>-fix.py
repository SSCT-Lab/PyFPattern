def actionEcdsaSign(self, to, data, privatekey=None):
    if (privatekey is None):
        privatekey = self.user.getAuthPrivatekey(self.site.address)
    self.response(to, CryptBitcoin.sign(data.encode('utf8'), privatekey))
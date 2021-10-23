

def actionEcdsaSign(self, to, data, privatekey=0):
    if (type(privatekey) is int):
        privatekey = self.user.getEncryptPrivatekey(self.site.address, privatekey)
    self.response(to, CryptBitcoin.sign(data.encode('utf8'), privatekey))

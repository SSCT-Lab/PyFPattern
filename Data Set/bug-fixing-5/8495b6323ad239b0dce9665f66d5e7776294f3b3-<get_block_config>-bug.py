def get_block_config(self, path):
    block = self.get_block(path)
    return dumps(block, 'config')
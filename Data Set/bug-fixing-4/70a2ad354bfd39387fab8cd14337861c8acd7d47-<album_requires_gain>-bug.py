def album_requires_gain(self, album):
    return (self.overwrite or any([(self.should_use_r128(item) and ((not item.r128_item_gain) or (not item.r128_album_gain))) for item in album.items()]) or any([((not self.should_use_r128(item)) and ((not item.rg_album_gain) or (not item.rg_album_peak))) for item in album.items()]))
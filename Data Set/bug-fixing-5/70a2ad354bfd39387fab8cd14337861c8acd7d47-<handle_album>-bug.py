def handle_album(self, album, write):
    "Compute album and track replay gain store it in all of the\n        album's items.\n\n        If ``write`` is truthy then ``item.write()`` is called for each\n        item. If replay gain information is already present in all\n        items, nothing is done.\n        "
    if (not self.album_requires_gain(album)):
        self._log.info('Skipping album {0}', album)
        return
    self._log.info('analyzing {0}', album)
    if (any([self.should_use_r128(item) for item in album.items()]) and all([self.should_use_r128(item) for item in album.items()])):
        raise ReplayGainError('Mix of ReplayGain and EBU R128 detectedfor some tracks in album {0}'.format(album))
    if any([self.should_use_r128(item) for item in album.items()]):
        if (self.r128_backend_instance == ''):
            self.init_r128_backend()
        backend_instance = self.r128_backend_instance
        store_track_gain = self.store_track_r128_gain
        store_album_gain = self.store_album_r128_gain
    else:
        backend_instance = self.backend_instance
        store_track_gain = self.store_track_gain
        store_album_gain = self.store_album_gain
    try:
        album_gain = backend_instance.compute_album_gain(album)
        if (len(album_gain.track_gains) != len(album.items())):
            raise ReplayGainError('ReplayGain backend failed for some tracks in album {0}'.format(album))
        store_album_gain(album, album_gain.album_gain)
        for (item, track_gain) in zip(album.items(), album_gain.track_gains):
            store_track_gain(item, track_gain)
            if write:
                item.try_write()
    except ReplayGainError as e:
        self._log.info('ReplayGain error: {0}', e)
    except FatalReplayGainError as e:
        raise ui.UserError('Fatal replay gain error: {0}'.format(e))
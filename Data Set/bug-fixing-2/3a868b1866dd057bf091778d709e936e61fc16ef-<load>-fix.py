

def load(self):
    self.unload()
    ff_opts = {
        'vn': True,
        'sn': True,
    }
    self._ffplayer = MediaPlayer(self.source, callback=self._player_callback, loglevel='info', ff_opts=ff_opts)
    player = self._ffplayer
    player.set_volume(self.volume)
    player.toggle_pause()
    self._state = 'paused'
    s = time.perf_counter()
    while ((player.get_metadata()['duration'] is None) and (not self.quitted) and ((time.perf_counter() - s) < 10.0)):
        time.sleep(0.005)

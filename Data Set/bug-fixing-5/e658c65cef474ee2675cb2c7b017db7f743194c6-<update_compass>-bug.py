def update_compass(self, *args):
    (x, y, z) = Hardware.magneticFieldSensorReading()
    needle_angle = (Vector(x, y).angle((0, 1)) + 90.0)
    if self._anim:
        self._anim.stop(self)
    self._anim = Animation(needle_angle=needle_angle, d=0.2, t='out_quad')
    self._anim.start(self)
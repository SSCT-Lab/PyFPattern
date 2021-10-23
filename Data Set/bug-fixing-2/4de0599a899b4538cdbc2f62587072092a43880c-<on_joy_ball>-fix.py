

def on_joy_ball(self, win, stickid, ballid, xvalue, yvalue):
    self.joy_motion('ball', stickid, ballid, (xvalue, yvalue))

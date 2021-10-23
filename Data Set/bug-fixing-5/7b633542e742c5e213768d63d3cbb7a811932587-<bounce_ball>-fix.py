def bounce_ball(self, ball):
    if (self.collide_widget(ball) and self.can_bounce):
        (vx, vy) = ball.velocity
        offset = ((ball.center_y - self.center_y) / (self.height / 2))
        bounced = Vector(((- 1) * vx), vy)
        vel = (bounced * 1.1)
        ball.velocity = (vel.x, (vel.y + offset))
        self.can_bounce = False
    elif ((not self.collide_widget(ball)) and (not self.can_bounce)):
        self.can_bounce = True
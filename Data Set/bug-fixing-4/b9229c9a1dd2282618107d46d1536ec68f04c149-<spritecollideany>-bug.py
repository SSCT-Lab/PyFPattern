def spritecollideany(sprite, group, collided=None):
    'finds any sprites in a group that collide with the given sprite\n\n    pygame.sprite.spritecollideany(sprite, group): return sprite\n\n    Given a sprite and a group of sprites, this will return return any single\n    sprite that collides with with the given sprite. If there are no\n    collisions, then this returns None.\n\n    If you don\'t need all the features of the spritecollide function, this\n    function will be a bit quicker.\n\n    Collided is a callback function used to calculate if two sprites are\n    colliding. It should take two sprites as values and return a bool value\n    indicating if they are colliding. If collided is not passed, then all\n    sprites must have a "rect" value, which is a rectangle of the sprite area,\n    which will be used to calculate the collision.\n\n    '
    if collided:
        for s in group:
            if collided(sprite, s):
                return s
    else:
        spritecollide = sprite.rect.colliderect
        for s in group:
            if spritecollide(s.rect):
                return s
    return None
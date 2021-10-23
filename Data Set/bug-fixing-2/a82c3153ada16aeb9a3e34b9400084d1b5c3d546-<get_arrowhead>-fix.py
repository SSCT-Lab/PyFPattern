

def get_arrowhead(self, direction, x, y, end):
    "Render individual arrow head.\n\n        direction (unicode): Arrow direction, 'left' or 'right'.\n        x (int): X-coordinate of arrow start point.\n        y (int): Y-coordinate of arrow start and end point.\n        end (int): X-coordinate of arrow end point.\n        RETURNS (unicode): Definition of the arrow head path ('d' attribute).\n        "
    if (direction == 'left'):
        (pos1, pos2, pos3) = (x, ((x - self.arrow_width) + 2), ((x + self.arrow_width) - 2))
    else:
        (pos1, pos2, pos3) = (end, ((end + self.arrow_width) - 2), ((end - self.arrow_width) + 2))
    arrowhead = (pos1, (y + 2), pos2, (y - self.arrow_width), pos3, (y - self.arrow_width))
    return 'M{},{} L{},{} {},{}'.format(*arrowhead)

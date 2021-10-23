def _draw_polygon(ax, vertices, alpha=0.4):
    import matplotlib.pyplot as plt
    polygon = Polygon(vertices, closed=True)
    p = PatchCollection([polygon], match_original=True, alpha=alpha)
    polygon_object = ax.add_collection(p)
    plt.draw()
    return polygon_object
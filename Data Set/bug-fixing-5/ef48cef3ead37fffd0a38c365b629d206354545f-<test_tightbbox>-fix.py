def test_tightbbox():
    (fig, ax) = plt.subplots()
    ax.set_xlim(0, 1)
    t = ax.text(1.0, 0.5, 'This dangles over end')
    renderer = fig.canvas.get_renderer()
    x1Nom0 = 9.035
    assert (abs((t.get_tightbbox(renderer).x1 - (x1Nom0 * fig.dpi))) < 2)
    assert (abs((ax.get_tightbbox(renderer).x1 - (x1Nom0 * fig.dpi))) < 2)
    assert (abs((fig.get_tightbbox(renderer).x1 - x1Nom0)) < 0.05)
    assert (abs((fig.get_tightbbox(renderer).x0 - 0.679)) < 0.05)
    t.set_in_layout(False)
    x1Nom = 7.333
    assert (abs((ax.get_tightbbox(renderer).x1 - (x1Nom * fig.dpi))) < 2)
    assert (abs((fig.get_tightbbox(renderer).x1 - x1Nom)) < 0.05)
    t.set_in_layout(True)
    x1Nom = 7.333
    assert (abs((ax.get_tightbbox(renderer).x1 - (x1Nom0 * fig.dpi))) < 2)
    assert (abs((ax.get_tightbbox(renderer, bbox_extra_artists=[]).x1 - (x1Nom * fig.dpi))) < 2)
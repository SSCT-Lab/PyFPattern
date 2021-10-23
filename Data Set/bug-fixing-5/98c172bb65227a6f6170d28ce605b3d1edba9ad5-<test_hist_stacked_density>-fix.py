@image_comparison(baseline_images=['hist_stacked_normed', 'hist_stacked_normed'])
def test_hist_stacked_density():
    d1 = np.linspace(1, 3, 20)
    d2 = np.linspace(0, 10, 50)
    (fig, ax) = plt.subplots()
    ax.hist((d1, d2), stacked=True, density=True)
    (fig, ax) = plt.subplots()
    with pytest.warns(UserWarning):
        ax.hist((d1, d2), stacked=True, normed=True)
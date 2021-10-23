@image_comparison(baseline_images=['hist_stacked_normed'], extensions=['png'])
def test_hist_stacked_density():
    d1 = np.linspace(1, 3, 20)
    d2 = np.linspace(0, 10, 50)
    (fig, ax) = plt.subplots()
    ax.hist((d1, d2), stacked=True, density=True)
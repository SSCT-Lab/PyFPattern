

@pytest.mark.parametrize('image, reference', [(image_rgb, template_rgb)])
def test_match_histograms(self, image, reference):
    "Assert that pdf of matched image is close to the reference's pdf for\n        all channels and all values of matched"
    matched = exposure.match_histograms(image, reference, multichannel=True)
    matched_pdf = self._calculate_image_empirical_pdf(matched)
    reference_pdf = self._calculate_image_empirical_pdf(reference)
    for channel in range(len(matched_pdf)):
        (reference_values, reference_quantiles) = reference_pdf[channel]
        (matched_values, matched_quantiles) = matched_pdf[channel]
        for (i, matched_value) in enumerate(matched_values):
            closest_id = np.abs((reference_values - matched_value)).argmin()
            assert_almost_equal(matched_quantiles[i], reference_quantiles[closest_id], decimal=1)

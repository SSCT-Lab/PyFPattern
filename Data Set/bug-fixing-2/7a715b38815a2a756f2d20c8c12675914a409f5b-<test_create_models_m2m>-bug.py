

def test_create_models_m2m(self):
    '\n        Modles are created via the m2m relation if the remote model has a\n        OneToOneField (#1064, #1506).\n        '
    f = Favorites(name='Fred')
    f.save()
    f.restaurants.set([self.r1])
    self.assertQuerysetEqual(f.restaurants.all(), ['<Restaurant: Demon Dogs the restaurant>'])

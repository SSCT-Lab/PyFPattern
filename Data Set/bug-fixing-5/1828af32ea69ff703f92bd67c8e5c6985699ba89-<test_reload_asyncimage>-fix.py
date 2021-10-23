def test_reload_asyncimage(self):
    from kivy.resources import resource_find
    from tempfile import mkdtemp
    from os import remove
    from shutil import copyfile, rmtree
    fn = resource_find('data/logo/kivy-icon-16.png')
    t = mkdtemp()
    source = join(t, 'source.png')
    copyfile(fn, source)
    image = AsyncImage(source=source)
    self.render(image, framecount=2)
    self.assertEqual(image.texture_size, [16, 16])
    remove(source)
    fn = resource_find('data/logo/kivy-icon-32.png')
    copyfile(fn, source)
    image.reload()
    self.render(image, framecount=2)
    self.assertEqual(image.texture_size, [32, 32])
    remove(source)
    rmtree(t)
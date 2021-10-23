def test_reload_asyncimage(self):
    from kivy.resources import resource_find
    from tempfile import mkdtemp
    from os import symlink, unlink
    from shutil import rmtree
    fn = resource_find('data/logo/kivy-icon-16.png')
    t = mkdtemp()
    source = join(t, 'source.png')
    symlink(fn, source)
    image = AsyncImage(source=source)
    self.render(image, framecount=2)
    self.assertEqual(image.texture_size, [16, 16])
    unlink(source)
    fn = resource_find('data/logo/kivy-icon-32.png')
    symlink(fn, source)
    image.reload()
    self.render(image, framecount=2)
    self.assertEqual(image.texture_size, [32, 32])
    unlink(source)
    rmtree(t)
def test_add(self):
    a5 = Article(headline='Django lets you create Web apps easily')
    msg = '"<Article: Django lets you create Web apps easily>" needs to have a value for field "id" before this many-to-many relationship can be used.'
    with self.assertRaisesMessage(ValueError, msg):
        getattr(a5, 'publications')
    a5.save()
    a5.publications.add(self.p1)
    self.assertQuerysetEqual(a5.publications.all(), ['<Publication: The Python Journal>'])
    a6 = Article(headline='ESA uses Python')
    a6.save()
    a6.publications.add(self.p1, self.p2)
    a6.publications.add(self.p3)
    a6.publications.add(self.p3)
    self.assertQuerysetEqual(a6.publications.all(), ['<Publication: Science News>', '<Publication: Science Weekly>', '<Publication: The Python Journal>'])
    with self.assertRaisesMessage(TypeError, "'Publication' instance expected, got <Article"):
        with transaction.atomic():
            a6.publications.add(a5)
    a6.publications.create(title='Highlights for Adults')
    self.assertQuerysetEqual(a6.publications.all(), ['<Publication: Highlights for Adults>', '<Publication: Science News>', '<Publication: Science Weekly>', '<Publication: The Python Journal>'])
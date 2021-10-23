

def setUp(self):
    self.au1 = Author.objects.create(name='Author 1')
    self.au2 = Author.objects.create(name='Author 2')
    self.a1 = Article.objects.create(headline='Article 1', pub_date=datetime(2005, 7, 26), author=self.au1, slug='a1')
    self.a2 = Article.objects.create(headline='Article 2', pub_date=datetime(2005, 7, 27), author=self.au1, slug='a2')
    self.a3 = Article.objects.create(headline='Article 3', pub_date=datetime(2005, 7, 27), author=self.au1, slug='a3')
    self.a4 = Article.objects.create(headline='Article 4', pub_date=datetime(2005, 7, 28), author=self.au1, slug='a4')
    self.a5 = Article.objects.create(headline='Article 5', pub_date=datetime(2005, 8, 1, 9, 0), author=self.au2, slug='a5')
    self.a6 = Article.objects.create(headline='Article 6', pub_date=datetime(2005, 8, 1, 8, 0), author=self.au2, slug='a6')
    self.a7 = Article.objects.create(headline='Article 7', pub_date=datetime(2005, 7, 27), author=self.au2, slug='a7')
    self.t1 = Tag.objects.create(name='Tag 1')
    self.t1.articles.add(self.a1, self.a2, self.a3)
    self.t2 = Tag.objects.create(name='Tag 2')
    self.t2.articles.add(self.a3, self.a4, self.a5)
    self.t3 = Tag.objects.create(name='Tag 3')
    self.t3.articles.add(self.a5, self.a6, self.a7)

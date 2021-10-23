def test_nonzero(self):
    num_src = 12
    types = ['torch.ByteTensor', 'torch.CharTensor', 'torch.ShortTensor', 'torch.IntTensor', 'torch.FloatTensor', 'torch.DoubleTensor', 'torch.LongTensor']
    shapes = [torch.LongStorage((12,)), torch.LongStorage((12, 1)), torch.LongStorage((1, 12)), torch.LongStorage((6, 2)), torch.LongStorage((3, 2, 2))]
    for t in types:
        tensor = torch.rand(num_src).mul(2).floor().type(t)
        for shape in shapes:
            tensor = tensor.clone().resize_(shape)
            dst1 = torch.nonzero(tensor)
            dst2 = tensor.nonzero()
            dst3 = torch.LongTensor()
            torch.nonzero(dst3, tensor)
            if (shape.size() == 1):
                dst = []
                for i in range(num_src):
                    if (tensor[i] != 0):
                        dst += [i]
                self.assertEqual(dst1.select(1, 0), torch.LongTensor(dst), 0)
                self.assertEqual(dst2.select(1, 0), torch.LongTensor(dst), 0)
                self.assertEqual(dst3.select(1, 0), torch.LongTensor(dst), 0)
            elif (shape.size() == 2):
                for i in range(dst1.size(0)):
                    self.assertNotEqual(tensor[(dst1[(i, 0)], dst1[(i, 1)])], 0)
            elif (shape.size() == 3):
                for i in range(dst1.size(0)):
                    self.assertNotEqual(tensor[(dst1[(i, 0)], dst1[(i, 1)], dst1[(i, 2)])], 0)
def test_consolidate_inplace(self):
    frame = self.frame.copy()
    for letter in range(ord('A'), ord('Z')):
        self.frame[chr(letter)] = chr(letter)
def test_consolidate_inplace(self, float_frame):
    frame = float_frame.copy()
    for letter in range(ord('A'), ord('Z')):
        float_frame[chr(letter)] = chr(letter)
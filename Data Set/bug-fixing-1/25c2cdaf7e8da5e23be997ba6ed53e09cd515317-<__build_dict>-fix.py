

def __build_dict(tar_file, dict_size, save_path, lang):
    word_dict = defaultdict(int)
    with tarfile.open(tar_file, mode='r') as f:
        for line in f.extractfile('wmt16/train'):
            line = cpt.to_text(line)
            line_split = line.strip().split('\t')
            if (len(line_split) != 2):
                continue
            sen = (line_split[0] if (lang == 'en') else line_split[1])
            for w in sen.split():
                word_dict[w] += 1
    with open(save_path, 'wb') as fout:
        fout.write(cpt.to_bytes(('%s\n%s\n%s\n' % (START_MARK, END_MARK, UNK_MARK))))
        for (idx, word) in enumerate(sorted(six.iteritems(word_dict), key=(lambda x: x[1]), reverse=True)):
            if ((idx + 3) == dict_size):
                break
            fout.write(cpt.to_bytes(word[0]))
            fout.write(cpt.to_bytes('\n'))

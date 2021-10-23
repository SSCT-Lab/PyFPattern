

def write_worker(q_out, fname, working_dir):
    pre_time = time.time()
    count = 0
    fname_rec = os.path.basename(fname)
    fname_rec = (os.path.splitext(fname)[0] + '.rec')
    fout = open((fname + '.tmp'), 'w')
    record = mx.recordio.MXRecordIO(os.path.join(working_dir, fname_rec), 'w')
    while True:
        deq = q_out.get()
        if (deq is None):
            break
        (s, item) = deq
        record.write(s)
        line = ('%d\t' % item[0])
        for j in item[2:]:
            line += ('%f\t' % j)
        line += ('%s\n' % item[1])
        fout.write(line)
        if ((count % 1000) == 0):
            cur_time = time.time()
            print('time:', (cur_time - pre_time), ' count:', count)
            pre_time = cur_time
        count += 1
    fout.close()
    os.remove(fname)
    os.rename((fname + '.tmp'), fname)

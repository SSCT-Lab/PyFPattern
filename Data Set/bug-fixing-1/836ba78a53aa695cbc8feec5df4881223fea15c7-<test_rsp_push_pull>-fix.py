

@with_seed()
@unittest.skipIf((mx.context.num_gpus() < 2), 'test_rsp_push_pull needs more than 1 GPU')
def test_rsp_push_pull():

    def check_rsp_push_pull(kv_type, sparse_pull, is_push_cpu=True):
        kv = init_kv_with_str('row_sparse', kv_type)
        kv.init('e', mx.nd.ones(shape).tostype('row_sparse'))
        push_ctxs = [(mx.cpu(i) if is_push_cpu else mx.gpu(i)) for i in range(2)]
        kv.push('e', [mx.nd.ones(shape, ctx=context).tostype('row_sparse') for context in push_ctxs])

        def check_rsp_pull(kv, ctxs, sparse_pull, is_same_rowid=False, use_slice=False):
            count = len(ctxs)
            num_rows = shape[0]
            row_ids = []
            all_row_ids = np.arange(num_rows)
            vals = [mx.nd.sparse.zeros(shape=shape, ctx=ctxs[i], stype='row_sparse') for i in range(count)]
            if is_same_rowid:
                row_id = np.random.randint(num_rows, size=num_rows)
                row_ids = ([mx.nd.array(row_id)] * count)
            elif use_slice:
                total_row_ids = mx.nd.array(np.random.randint(num_rows, size=(count * num_rows)))
                row_ids = [total_row_ids[(i * num_rows):((i + 1) * num_rows)] for i in range(count)]
            else:
                for i in range(count):
                    row_id = np.random.randint(num_rows, size=num_rows)
                    row_ids.append(mx.nd.array(row_id))
            row_ids_to_pull = (row_ids[0] if ((len(row_ids) == 1) or is_same_rowid) else row_ids)
            vals_to_pull = (vals[0] if (len(vals) == 1) else vals)
            kv.row_sparse_pull('e', out=vals_to_pull, row_ids=row_ids_to_pull)
            for (val, row_id) in zip(vals, row_ids):
                retained = val.asnumpy()
                excluded_row_ids = np.setdiff1d(all_row_ids, row_id.asnumpy())
                for row in range(num_rows):
                    expected_val = np.zeros_like(retained[row])
                    expected_val += (0 if (row in excluded_row_ids) else 2)
                    assert_almost_equal(retained[row], expected_val)
            if (sparse_pull is True):
                kv.pull('e', out=vals_to_pull, ignore_sparse=False)
                for val in vals:
                    retained = val.asnumpy()
                    expected_val = np.zeros_like(retained)
                    expected_val[:] = 2
                    assert_almost_equal(retained, expected_val)
        check_rsp_pull(kv, [mx.gpu(0)], sparse_pull)
        check_rsp_pull(kv, [mx.cpu(0)], sparse_pull)
        check_rsp_pull(kv, [mx.gpu((i // 2)) for i in range(4)], sparse_pull)
        check_rsp_pull(kv, [mx.gpu((i // 2)) for i in range(4)], sparse_pull, is_same_rowid=True)
        check_rsp_pull(kv, [mx.cpu(i) for i in range(4)], sparse_pull)
        check_rsp_pull(kv, [mx.cpu(i) for i in range(4)], sparse_pull, is_same_rowid=True)
        check_rsp_pull(kv, [mx.gpu((i // 2)) for i in range(4)], sparse_pull, use_slice=True)
        check_rsp_pull(kv, [mx.cpu(i) for i in range(4)], sparse_pull, use_slice=True)
    envs = ['', '1']
    key = 'MXNET_KVSTORE_USETREE'
    for val in envs:
        with EnvManager(key, val):
            if (val is '1'):
                sparse_pull = False
            else:
                sparse_pull = True
            check_rsp_push_pull('local', sparse_pull)
            check_rsp_push_pull('device', sparse_pull)
            check_rsp_push_pull('device', sparse_pull, is_push_cpu=False)

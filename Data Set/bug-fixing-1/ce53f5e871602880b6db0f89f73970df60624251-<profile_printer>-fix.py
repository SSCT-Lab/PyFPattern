

@theano.compile.profiling.register_profiler_printer
def profile_printer(message, compile_time, fct_call_time, apply_time, apply_cimpl, outputs_size, file):
    if any([(isinstance(node.op, Scan) and (v > 0)) for (node, v) in apply_time.items()]):
        print('', file=file)
        print('Scan overhead:', file=file)
        print('<Scan op time(s)> <sub scan fct time(s)> <sub scan op time(s)> <sub scan fct time(% scan op time)> <sub scan op time(% scan op time)> <node>', file=file)
        total_super_scan_time = 0
        total_scan_fct_time = 0
        total_scan_op_time = 0
        for (node, v) in iteritems(apply_time):
            if (isinstance(node.op, Scan) and (not node.op.fn.profile)):
                print("  One scan node do not have its inner profile enabled. If you enable Theano profiler with 'theano.function(..., profile=True)', you must manually enable the profiling for each scan too: 'theano.scan_module.scan(...,profile=True)'. Or use Theano flag 'profile=True'.", file=file)
            elif (isinstance(node.op, Scan) and node.op.fn.profile):
                if (v > 0):
                    scan_fct_time = node.op.fn.profile.call_time
                    scan_op_time = sum(node.op.fn.profile.apply_time.values())
                    total_super_scan_time += v
                    total_scan_fct_time += scan_fct_time
                    total_scan_op_time += scan_op_time
                    print(('      %5.1fs  %5.1fs  %5.1fs  %5.1f%%  %5.1f%%' % (v, scan_fct_time, scan_op_time, ((scan_fct_time / v) * 100), ((scan_op_time / v) * 100))), node, file=file)
                else:
                    print(' The node took 0s, so we can not compute the overhead', node, file=file)
        if (total_super_scan_time == 0):
            print('  No scan have its inner profile enabled.', file=file)
        else:
            print(('total %5.1fs  %5.1fs  %5.1fs  %5.1f%%  %5.1f%%' % (total_super_scan_time, total_scan_fct_time, total_scan_op_time, ((total_scan_fct_time / total_super_scan_time) * 100), ((total_scan_op_time / total_super_scan_time) * 100))), file=file)

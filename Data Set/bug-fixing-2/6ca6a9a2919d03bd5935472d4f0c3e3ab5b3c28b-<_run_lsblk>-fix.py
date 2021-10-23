

def _run_lsblk(self, lsblk_path):
    args = ['--list', '--noheadings', '--paths', '--output', 'NAME,UUID', '--exclude', '2']
    cmd = ([lsblk_path] + args)
    (rc, out, err) = self.module.run_command(cmd)
    return (rc, out, err)

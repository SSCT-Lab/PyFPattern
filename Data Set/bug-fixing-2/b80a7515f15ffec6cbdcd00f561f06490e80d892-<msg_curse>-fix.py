

def msg_curse(self, args=None):
    'Return the dict to display in the curse interface.'
    ret = []
    if ((not self.stats) or (self.stats == []) or self.is_disable()):
        return ret
    if (len(self.stats) == 1):
        gpu_stats = self.stats[0]
        header = '{} {}'.format('GPU', gpu_stats['name'])
        msg = header[:16]
        ret.append(self.curse_add_line(msg, 'TITLE'))
        ret.append(self.curse_new_line())
        msg = '{:8}'.format('proc:')
        ret.append(self.curse_add_line(msg))
        msg = '{:>7d}%'.format(int(gpu_stats['proc']))
        ret.append(self.curse_add_line(msg, self.get_views(item=gpu_stats[self.get_key()], key='proc', option='decoration')))
        ret.append(self.curse_new_line())
        msg = '{:8}'.format('mem:')
        ret.append(self.curse_add_line(msg))
        if (gpu_stats['mem'] is None):
            msg = '{:>8}'.format('N/A')
        else:
            msg = '{:>7d}%'.format(int(gpu_stats['mem']))
        ret.append(self.curse_add_line(msg, self.get_views(item=gpu_stats[self.get_key()], key='mem', option='decoration')))
    else:
        header = '{} {}'.format(len(self.stats), 'GPUs')
        msg = header[:16]
        ret.append(self.curse_add_line(msg, 'TITLE'))
        for gpu_stats in self.stats:
            ret.append(self.curse_new_line())
            msg = '{}: {:>3}% mem: {:>3}%'.format(gpu_stats['gpu_id'], gpu_stats['proc'], gpu_stats['proc'])
            ret.append(self.curse_add_line(msg))
    return ret

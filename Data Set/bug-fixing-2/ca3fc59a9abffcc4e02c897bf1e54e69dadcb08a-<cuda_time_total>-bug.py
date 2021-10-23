

@property
def cuda_time_total(self):
    return sum((kinfo[1].elasped_us() for kinfo in self.kernels))

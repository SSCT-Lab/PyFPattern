

@property
def cuda_time_total(self):
    return sum((kinfo[1].elapsed_us() for kinfo in self.kernels))

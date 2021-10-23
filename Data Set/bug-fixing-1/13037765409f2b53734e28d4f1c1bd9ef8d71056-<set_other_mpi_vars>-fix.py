

def set_other_mpi_vars(environ_cp):
    'Set other MPI related variables.'
    mpi_home = environ_cp.get('MPI_HOME')
    symlink_force(('%s/include/mpi.h' % mpi_home), 'third_party/mpi/mpi.h')
    if os.path.exists(os.path.join(mpi_home, 'include/mpi_portable_platform.h')):
        symlink_force(os.path.join(mpi_home, 'include/mpi_portable_platform.h'), 'third_party/mpi/mpi_portable_platform.h')
        sed_in_place('third_party/mpi/mpi.bzl', 'MPI_LIB_IS_OPENMPI = False', 'MPI_LIB_IS_OPENMPI = True')
    else:
        symlink_force(os.path.join(mpi_home, 'include/mpio.h'), 'third_party/mpi/mpio.h')
        symlink_force(os.path.join(mpi_home, 'include/mpicxx.h'), 'third_party/mpi/mpicxx.h')
        sed_in_place('third_party/mpi/mpi.bzl', 'MPI_LIB_IS_OPENMPI = True', 'MPI_LIB_IS_OPENMPI = False')
    if os.path.exists(os.path.join(mpi_home, 'lib/libmpi.so')):
        symlink_force(os.path.join(mpi_home, 'lib/libmpi.so'), 'third_party/mpi/libmpi.so')
    elif os.path.exists(os.path.join(mpi_home, 'lib64/libmpi.so')):
        symlink_force(os.path.join(mpi_home, 'lib64/libmpi.so'), 'third_party/mpi/libmpi.so')
    elif os.path.exists(os.path.join(mpi_home, 'lib32/libmpi.so')):
        symlink_force(os.path.join(mpi_home, 'lib32/libmpi.so'), 'third_party/mpi/libmpi.so')
    else:
        raise ValueError(('Cannot find the MPI library file in %s/lib or %s/lib64 or %s/lib32' % (mpi_home, mpi_home, mpi_home)))

import torch
import os
import pkg_resources


MOD_NAME = 'frnn'
PKG_NAME = MOD_NAME + '-chenn'


pkg = pkg_resources.working_set.by_key[PKG_NAME]
so_path = os.path.join(pkg.location, MOD_NAME, 'lib' + MOD_NAME + '.so' )
torch.ops.load_library(so_path)


def get_frnn(*args, **kwargs):
    return torch.ops.my_ops.frnn_ts_kernel(*args, **kwargs)
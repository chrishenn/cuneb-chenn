import torch
import os
import pkg_resources
from dotenv import load_dotenv

load_dotenv()

PKG_NAME = os.getenv('PKG_NAME')
MOD_NAME = os.getenv('MOD_NAME')
OPS_NAME = os.getenv('OPS_NAME')

pkg = pkg_resources.working_set.by_key[PKG_NAME]
so_path = os.path.join(pkg.location, MOD_NAME, 'lib' + MOD_NAME + '.so' )
torch.ops.load_library(so_path)


def get(*args, **kwargs):
    func_string = 'torch.ops.' + OPS_NAME +'.' + MOD_NAME
    return eval(func_string)(*args, **kwargs)



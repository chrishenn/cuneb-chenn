import torch
import os

if __name__ == "__main__":
    so_path = '/cuneb/build/libcuneb.so'
    torch.ops.load_library(so_path)
    torch.ops.cuneb_ops.cuneb
    print("donce")
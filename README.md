# Example Pip Pytorch-CUDA Library Package

An example to install and expose a cuda/c++ pytorch-torchlib extension as its own pip package. Provides versioning for cuda libraries via packaging.

This structure does fully support including the packaged CUDA/C++ torch extension into a torchscript-managed module or operator. The benefits of compiling a python model into torchscript are many - see the tutorial for a nice list [(extending torchscript tutorial)](https://pytorch.org/tutorials/advanced/torch_script_custom_ops.html) - but my main interest is in the performance and scalability offered by serializing a model to disk (which can be loaded into multiple processes), and running a model in a python-free environment.

We choose CMake compilation for our cuda/c++ library, rather than setuptools. CMake allows for fewer headaches in the extension's project structure - finding includes, headers, and source files arbitrarily - and generally is worth the effort of including another build tool. As the [extending torchscript tutorial](https://pytorch.org/tutorials/advanced/torch_script_custom_ops.html) casually mentions, using setuptools to build a plain shared library can be "slightly quirky".

### Details

In the pkg/module/.env file, there are PKG_NAME MOD_NAME OPS_NAME definitions. These definitions are used to build the package, and are then installed with the package to help python find and call the correct shared-object file.

There are two additional places where the module's names must be hardcoded; one at the top of setup.py, and one in pkg/module/module.cpp. These module names must agree with those in the .env file.

The LIBTORCH_PATH definition is also found in the .env file. This variable should point to the absolute path of your unzipped libtorch library folder (you can of course still override this by specifying `-DCMAKE_PREFIX_PATH=/path/to/libtorch` at terminal if building manually).

To install, open a shell in the package folder. Run `pip install .`

This example includes libtorch, pytorch, cuda-11, cudnn-8.4.0.27, and gcc~9 dependencies.



## ManyLinux

Run `sudo sh run-manylinux.sh` to start building manylinux wheels.

`run-manylinux.sh` specifies a manylinux docker container inside which the manylinux wheels are built (and tested - todo). You'll need docker installed. I've found manylinux containers built with CUDA installed [(ameli/manylinux-cuda)](https://github.com/ameli/manylinux-cuda) which is very helpful, because the build is cantankerous and slow. However, it would be nice to build a version with an appropriate cudnn installed (todo). 

`build-wheels.sh` is run inside the container to build and format the wheels.

### Notes
Use a machine with more than 64 GB of ram (maybe more like 256 GB) - push this to the build server (super easy CI integration with travis - see [the manylinux github tutorial](https://github.com/pypa/python-manylinux-demo) for info). I copied a starting point for the two shell scripts from the same.   

Well this is awkward. This simple project build with Cuda 11 and cudnn dependencies results in a .whl file that is too large for upload to pypi. This appears to be a problem that they have encountered more and more often, specifically calling out Cuda-11 dependencies as inflating the .whl size [(see here)](https://discuss.python.org/t/what-to-do-about-gpus-and-the-built-distributions-that-support-them/7125). As mentioned in that discussion, Pytorch has to host and distribute their own python packages because the infrastructure is just too expensive for Pypa. 

This packaging exercise is still worthwhile for learning about CI. In particular, the cpu and memory requirements are quite high - just to build this simple little package! Suitable for an internal build server only. Don't send these packages over the web unless you really have to.



 ## TODO

- sudo sh run-manylinux.sh
- python -m build
- move the files you want to distribute into ./dist/
- twine upload --skip-existing --verbose -p $token -u __token__ --repository "cuneb-chenn" --repository-url https://upload.pypi.org/legacy/ dist/*


- TODO: --use-feature=in-tree-build (will be default behavior in future. See if it breaks the package)
- TODO: add attribution for custominstall setup classes (stackoverflow)
- TODO: add tests
- TODO: build-wheels.sh ends with an EOF error, but runs successfully to completion. Would be nice to finish with a success message rather than an error.
- TODO: local cudnn install in build-wheel.sh
- TODO: figure out what those -pypy-something binaries are in build-wheels.h


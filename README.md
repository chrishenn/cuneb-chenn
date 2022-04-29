# A first pypi package

To install and expose a cuda/c++ torch extension as its own pip package. Provides versioning for cuda libraries via packaging.

In the pkg/module/.env file, there are PKG_NAME MOD_NAME OPS_NAME definitions. These definitions are used to build the package, and are then installed with the package to help python find and call the correct shared-object file.

There are two places where the module's name must be hardcoded, in addition to the .env file; one at the top of setup.py, and one in pkg/module/module.cpp. These module names must agree with those in the .env file.

The LIBTORCH_PATH definition is also found in the .env file. This variable should point to the absolute path of your unzipped libtorch library folder (you can of course still override this by specifying -DCMAKE_PREFIX_PATH=/path/to/libtorch at terminal).

- TODO: put module into src directory
- TODO: add test directory
- 
- TODO: upload to pypi for easy online installation
- TODO: --use-feature=in-tree-build
- TODO: add attribution for custominstall setup classes (stackoverflow)


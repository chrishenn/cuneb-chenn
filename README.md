# A first pypi package

To install and expose a cuda/c++ torch extension as its own pip package. Provides versioning for cuda libraries via packaging.

The folder containing the __init__.py which exposes the "get" function, MUST be named relative to the package folder. If the package folder is "cuneb-chenn", then the included module would be "cuneb".

- TODO: put frnn module into src directory
- TODO: add test directory with package tests that can run automatically via pip
- TODO: upload to pypi for easy online installation
- TODO: expose the module name and package name globally so that it doesn't need to be set multiple times

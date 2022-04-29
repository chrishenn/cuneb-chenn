import os
import subprocess
import shutil
import sys

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install

from dotenv import load_dotenv

## Hardcode project names here
## this path should point to the .env file in the module, relative to here (setup.py)
load_dotenv(dotenv_path='./cuneb/.env', override=True)

PKG_NAME = os.getenv('PKG_NAME')
MOD_NAME = os.getenv('MOD_NAME')
OPS_NAME = os.getenv('OPS_NAME')



def check_for_cmake():

    CMAKE_EXE = os.environ.get('CMAKE_EXE', shutil.which('cmake'))
    if not CMAKE_EXE:
        print('cmake executable not found. '
              'Set CMAKE_EXE environment or update your path')
        sys.exit(1)

    return CMAKE_EXE


class CMakeExtension(Extension):
    """
    setuptools.Extension for cmake
    """

    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuildExt(build_ext):
    """
    setuptools build_ext which builds using cmake & make
    You can add cmake args with the CMAKE_COMMON_VARIABLES environment variable
    """

    def build_extension(self, ext):

        if isinstance(ext, CMakeExtension):
            CMAKE_EXE = check_for_cmake()
            output_dir = os.path.join( os.path.abspath( os.path.dirname(self.get_ext_fullpath(ext.name)) ), ext.name)

            build_type = 'Debug' if self.debug else 'Release'
            cmake_args = [CMAKE_EXE,
                          ext.sourcedir,
                          '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + output_dir,
                          '-DCMAKE_BUILD_TYPE=' + build_type]
            cmake_args.extend(
                [x for x in
                 os.environ.get('CMAKE_COMMON_VARIABLES', '').split(' ')
                 if x])

            env = os.environ.copy()
            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)

            subprocess.check_call(cmake_args,
                                  cwd=self.build_temp,
                                  env=env)
            subprocess.check_call(['make', '-j'+str(os.cpu_count() // 2), ext.name],
                                  cwd=self.build_temp,
                                  env=env)

            print()
        else:
            super().build_extension(ext)

class CustomInstall(install):

    def run(self):
        install.run(self)



setup(
    name=PKG_NAME,
    version='0.0.1',
    description='',
    url='',
    author='',
    author_email='',
    license='',

    packages=[MOD_NAME],
    ext_modules=[CMakeExtension(MOD_NAME, sourcedir=MOD_NAME)],
    cmdclass={
        'install': CustomInstall,
        'build_ext': CMakeBuildExt,
    },
    package_data={MOD_NAME : [".env"]},

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: GPU :: NVIDIA CUDA',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)





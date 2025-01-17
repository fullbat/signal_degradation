import os

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

package_name = 'signal_degradation'

def get_extension():
    signal_degradation = Extension(
        name='signal_degradation',
        sources=['signal_degradation.pyx'],
        include_dirs=['.'],
        libraries=['stdc++'],
        extra_compile_args=['-w', '-std=c++11'],
        language='c++'
    )
    return [signal_degradation]

class CustomBuildExtCommand(build_ext):
    """ build_ext command to use when numpy headers are needed. """
    def run(self):
        # Now that the requirements are installed, get everything from numpy
        from multiprocessing import cpu_count

        from Cython.Build import cythonize
        from numpy import get_include

        # Add everything requires for build
        self.swig_opts = None
        self.include_dirs = [get_include()]
        self.distribution.ext_modules[:] = cythonize( self.distribution.ext_modules, build_dir='build' )

        # if not specified via '-j N' option, set compilation using max number of cores
        if self.parallel is None:
            self.parallel = cpu_count()
        print( f'Parallel compilation using {self.parallel} threads' )

        # Call original build_ext command
        build_ext.finalize_options(self)
        build_ext.run(self)

# create the 'build' directory
if not os.path.exists('build'):
    os.makedirs('build')

# install the package
setup(
    cmdclass={'build_ext': CustomBuildExtCommand},
    ext_modules=get_extension()
)
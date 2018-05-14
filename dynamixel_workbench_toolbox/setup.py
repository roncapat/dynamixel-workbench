
from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

setup_args = generate_distutils_setup (
    packages=['dynamixel_workbench_toolbox'],
    package_dir={'': 'python'},
    install_requires=['dynamixel_sdk']
)

setup(**setup_args)

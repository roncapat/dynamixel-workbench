
from setuptools import setup

setup(
    name='dynamixel_workbench_toolbox',
    version='0.2.4',
    packages=['dynamixel_sdk'],
    package_dir={'': 'src'},
    license='Apache 2.0',
    description='Dynamixel Workbench Toolbox',
    url='https://github.com/ROBOTIS-GIT/dynamixel-workbench',
    author='Marco Lapolla, Patrick Roncagliolo',
    author_email='marco.lapolla.iic96@gmail.com, ronca.pat@gmail.com',
    install_requires=['dynamixel_sdk']
)

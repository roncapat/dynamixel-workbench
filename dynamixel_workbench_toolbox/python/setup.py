
from setuptools import setup

setup(
    name='dynamixel_workbench_toolbox',
    version='3.6.0',
    packages=['dynamixel_sdk'],
    package_dir={'': 'src'},
    license='Apache 2.0',
    description='Dynamixel Workbench Toolbox',
    url='https://github.com/ROBOTIS-GIT/dynamixel-workbench',
    author=['Marco Lapolla', 'Patrick Roncagliolo'],
    author_email='ronca.pat@gmail.com',
    install_requires=['dynamixel_sdk']
)

"""Setup file for the python-rebase package"""

from setuptools import find_packages, setup

setup(
    name='python-rebase',
    packages=find_packages(include=['python-rebase']),
    version='1.0.0',
    description='Python implementation of the ReBase API',
    author='Tiago Trotta',
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.4.0'],
    test_suite='tests',
)

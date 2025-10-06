from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    
setup(
    name='hotel_reservations',
    version='0.1',
    author='Saheed',
    packages=find_packages(),
    install_requires = requirements,
)
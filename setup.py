from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open('requirements.txt', 'r') as file:
    INSTALL_REQUIRES = file.read().splitlines()

# Packages to include
PACKAGES = find_packages()

# Package setup
setup(
    NAME='latam-challenge',
    VERSION='1.0.0',
    AUTHOR='Edgard Abarcas Vidal',
    DESCRIPTION='Software Engineer (ML & LLMs) Application Challenge',
    EMAIL = "elav.1995@gmail.com",
    URL = "https://https://github.com/Elav95/latam-challenge",
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES
)
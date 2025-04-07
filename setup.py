# python-utils-and-tools/setup.py

from setuptools import setup, find_packages
import os

# Read dependencies from requirements.txt files
def read_requirements(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Combine dependencies from all requirements.txt files
install_requires = []

# # Root-level requirements (if exists)
# try:
#     install_requires.extend(read_requirements('requirements.txt'))
# except FileNotFoundError:
#     pass

# rag requirements
install_requires.extend(read_requirements('src/rag/requirements.txt'))
# utils requirements
install_requires.extend(read_requirements('src/utils/requirements.txt'))

setup(
    name="python-utils-and-tools",
    version="0.1.0",
    package_dir={"pyut": "src"},  # Map the pyut package to the src directory
    packages=["pyut", "pyut.rag", "pyut.utils"],  # Explicitly list the packages
    install_requires=install_requires,
    author="Mohamed Nagy",
    author_email="n4jidx@example.com",
    description="A collection of Python utilities and tools",
    long_description=open('README.md').read() if os.path.exists('README.md') else "",
    long_description_content_type="text/markdown",
)

# # In main_dir
# pip uninstall python-utils-and-tools -y

# # In main_dir
# pip install ./python-utils-and-tools
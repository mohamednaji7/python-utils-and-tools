# python-utils-and-tools/setup.py

from setuptools import setup, find_packages
import os

# get os environment variable INSTALL_DEPENDENCIES
INSTALL_DEPENDENCIES = os.environ.get("INSTALL_DEPENDENCIES")

# Read dependencies from requirements.txt files
def read_requirements(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Combine dependencies from all requirements.txt files
all_deps = set()

# # Root-level requirements (if exists)
# try:
#     install_requires.extend(read_requirements('requirements.txt'))
# except FileNotFoundError:
#     pass

if INSTALL_DEPENDENCIES:
    # rag requirements
    all_deps.update(read_requirements('src/rag/requirements.txt'))
    # utils requirements
    all_deps.update(read_requirements('src/utils/requirements.txt'))
    # transcribe requirements
    all_deps.update(read_requirements('src/transcribe/requirements.txt'))


setup(
    name="python-utils-and-tools",
    version="0.1.0",
    packages=["pyut", "pyut.rag", "pyut.utils", "pyut.transcribe"],  # Explicitly list the packages
    # packages=find_packages(where="src"),  # This will find pyut, pyut.rag, pyut.utils, etc.
    package_dir={"pyut": "src"},  # Map the pyut package to the src directory

    author="Mohamed Nagy",
    author_email="n4jidx@example.com",
    description="A collection of Python utilities and tools",
    long_description=open('README.md').read() if os.path.exists('README.md') else "",
    long_description_content_type="text/markdown",
    install_requires=list(all_deps),
)

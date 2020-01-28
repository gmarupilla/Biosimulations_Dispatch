""" Setup file for the Biosimulations dispatch Package

:Author: Bilal Shaikh < bilalshaikh42@gmail.com >
:Date: 2020-01-25
:Copyright: 2020, Karr Lab
:License: MIT
"""


import re
import setuptools
import os
import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    import pkg_utils
except ImportError:
    install("pkg_utils")
    import pkg_utils

name = 'biosimulations_dispatch'
dirname = os.path.dirname(__file__)
package_data = {
    name: [
        'VERSION'
    ],
}


# get package metadata
pkg_utils.convert_readme_md_to_rst(dirname)
md = pkg_utils.get_package_metadata(dirname, name)

# remove readme.rst
if os.path.exists("README.rst"):
    os.remove("README.rst")

# get version from _version.py file
VERSIONFILE = "biosimulations_dispatch/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    __version__ = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))
# install package
setuptools.setup(
    name=name,
    version=__version__,
    description='A python package for dispatching the biosimulations database',
    long_description=md.long_description,
    url="https://github.com/reproducible-biomedical-modeling/" + name,
    download_url='https://github.com/reproducible-biomedical-modeling/' + name,
    author="Center for Reproducible Biomedical Modeling",
    author_email="info@reproduciblebiomodels.org",
    license="MIT",
    keywords='',
    packages=setuptools.find_packages(
        exclude=[
            'tests',
            'tests.*']),
    package_data=md.package_data,
    install_requires=md.install_requires,
    extras_require=md.extras_require,
    tests_require=md.tests_require,
    dependency_links=md.dependency_links,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts': ["biosimulations_dispatch = biosimulations_dispatch.__main__:main"],
    },
)

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

version = "1.1.0"

setup(
    name='pdfutils',
    version=version,
    description='python tool to manipulate pdf file',
    author='smileboywtu',
    author_email='smileboywtu@gmail.com',
    url='https://github.com/smileboywtu/pdfutils',
    include_package_data=True,
    packages=[
        'pdfutils',
    ],
    install_requires=[
        'click', 'reportlab', 'pypdf2',
    ],
    entry_points={
        'console_scripts':
            ['pdfutils=pdfutils:main']
    }
)
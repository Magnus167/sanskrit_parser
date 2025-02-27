"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding

from os import path
import codecs

def read(rel_path):
    here = path.abspath(path.dirname(__file__))
    with codecs.open(path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
long_description = ''
try:
    import pypandoc

    long_description = pypandoc.convert_file('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''

setup(
  name='sanskrit_parser',

  # Versions should comply with PEP440.  For a discussion on single-sourcing
  # the version across setup.py and the project code, see
  # https://packaging.python.org/en/latest/single_source_version.html
  # version='0.2.2-post0',
    version=get_version("sanskrit_parser/__init__.py"),
  description='Tools for lexical and morphological analysis of Sanskrit',
  long_description=long_description,

  # The project's main homepage.
  url='https://github.com/kmadathil/sanskrit_parser',

  # Author details
  author='Sanskrit programmers',
  author_email='sanskrit-programmers@googlegroups.com',

  # Choose your license
  license='MIT',

  # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
  classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    # Left commented as this category doesn't exist
    # 'Natural Language :: Sanskrit',
    'Topic :: Text Processing :: Linguistic',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],

  # What does your project relate to?
  keywords='sanskrit samskritam',

  # You can just specify the packages manually here if your project is
  # simple. Or you can use find_packages().
  packages=find_packages(exclude=['contrib', 'docs', 'tests', 'metrics']),

  # Alternatively, if you want to distribute just a my_module.py, uncomment
  # this:
  #   py_modules=["my_module"],

  # List run-time dependencies here.  These will be installed by pip when
  # your project is installed. For an analysis of "install_requires" vs pip's
  # requirements files see:
  # https://packaging.python.org/en/latest/requirements.html
  install_requires=['indic_transliteration!=1.9.5,!=1.9.6', 'lxml', 'networkx', 'tinydb',
                    'six', 'flask', 'flask_restx', 'flask_cors',
                    'jsonpickle', 'sanskrit_util', 'sqlalchemy<1.4',
                    'pydot', 'pandas', 'xlrd', 'importlib_resources',
                    # Remove when https://github.com/python-restx/flask-restx/issues/460 is fixed
                    'werkzeug==2.1.2'
                    ],

  # List additional groups of dependencies here (e.g. development
  # dependencies). You can install these using the following syntax,
  # for example:
  # $ pip install -e .[dev,test]
  extras_require={
  #     'dev': ['check-manifest'],
  #     'test': ['pandas', 'xlrd'],
  },

  # If there are data files included in your packages that need to be
  # installed, specify them here.  If using Python 2.6 or less, then these
  # have to be included in MANIFEST.in as well.
  package_data={
       'sanskrit_parser': ['parser/sandhi_rules/*.txt', 'data/*'],
  },

  # Although 'package_data' is the preferred approach, in some case you may
  # need to place data files outside of your packages. See:
  # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
  # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
  # data_files=[('my_data', ['data/data_file'])],

  # scripts = ["scripts/sanskrit_parser"],
  # To provide executable scripts, use entry points in preference to the
  # "scripts" keyword. Entry points provide cross-platform support and allow
  # pip to create the appropriate form of executable for the target platform.
  entry_points={
       'console_scripts': [
           'sanskrit_parser=sanskrit_parser.cmd_line:cmd_line',
       ],
   },
)

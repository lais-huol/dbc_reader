import sys
from setuptools import setup

version = '0.1.0'

if len(sys.argv) >= 3 and sys.argv[1] == 'validate_tag':
    if sys.argv[2] != version:
        raise Exception(f"A versão TAG [{sys.argv[2]}] é diferente da versão no arquivo setup.py [{version}].")
    exit()

setup(**{
    "name": 'dbc_reader',
    "description": 'Utils classes to read DBC files, a DATASUS compressed DBF files',
    "long_description": 'Utils classes to read DBC files, a DATASUS compressed DBF files, that a distributed without compliance with the DBF or PKWare specification',
    "license": 'MIT',
    "author": 'Kelson da Costa Medeiros',
    "author_email": 'kelson.medeiros@lais.huol.ufrn.br',
    "packages": ['dbf_reader'],
    "include_package_data": True,
    "version": version,
    "download_url": f"https://github.com/lais-huol/dbc_reader/releases/tag/{version}",
    "url": 'https://github.com/lais-huol/dbc_reader',
    "keywords": ['DBF', 'DBC', 'reader', 'datasus', ],
    "python_requires": '>=3.7.0',
    "install_requires": ['dbf-reader>=0.2.2'],
    "classifiers": [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
})

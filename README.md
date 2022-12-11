# dbc_reader for python

Python utils classes to read **DATASUS** compressed DBF files (*.dbc), that a distributed without compliance with DBF and PKWare specification.

## How to use

### Install

```bash
pip install dbc_reader
```

### Fast mode

```python
from dbc_reader import DbcReader
rows = [row for row in DbcReader('my.dbc')]
```

### Full control

```python
from dbc_reader import DbcReader

with open("my.dbc", 'rb') as f:
    dbc_reader = DbcReader(f)

    # File info
    print(dbc_reader.encoding)
    print(dbc_reader.actual_record)
    print(dbc_reader.records)
    print(dbc_reader.last_update)
    print(dbc_reader.file_size)

    # Table info
    print(dbc_reader.definition.dbf_format)
    print(dbc_reader.definition.headerlen)
    print(dbc_reader.definition.numfields)
    print(dbc_reader.definition.record_size)
    print(dbc_reader.definition.terminator)
    print(dbc_reader.definition.actual_record)

    # Fields info
    for field in dbc_reader.definition.fields:
        print(field.order, field.name, field.type, field.size, field.decimals, field.flags)

    for row in DbcReader('my.dbc'):
        print(row)
```

## Development and test

```bash
docker build -t python_dbc_reader . 
docker run -it --rm -v "$PWD:/app" -w /app python_dbc_reader bash -c 'flake8 . --count --max-complexity=11 --max-line-length=404 --statistics && coverage run -m unittest tests && coverage report -m'
```
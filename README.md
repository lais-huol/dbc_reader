# dbf_reader for python

Python utils classes to read DBF files, specially **DATASUS** compressed DBF files, that a distributed without compliance with the specification.

## How to use

### Install

```bash
pip install dbf_reader
```

### Fast mode

```python
from dbf_reader import DbfReader
rows = [row for row in DbfReader('my.dbf')]
```

### Full control

```python
from dbf_reader import DbfReader

with open("my.dbf", 'rb') as f:
    dbf_reader = DbfReader(f)

    # File info
    print(dbf_reader.encoding)
    print(dbf_reader.actual_record)
    print(dbf_reader.records)
    print(dbf_reader.last_update)
    print(dbf_reader.file_size)

    # Table info
    print(dbf_reader.definition.dbf_format)
    print(dbf_reader.definition.headerlen)
    print(dbf_reader.definition.numfields)
    print(dbf_reader.definition.record_size)
    print(dbf_reader.definition.terminator)
    print(dbf_reader.definition.actual_record)

    # Fields info
    for field in dbf_reader.definition.fields:
        print(field.order, field.name, field.type, field.size, field.decimals, field.flags)

    for row in DbfReader('my.dbf'):
        print(row)
```

## Development and test

```bash
docker build -t python_dbc_reader . 
docker run -it --rm -v "$PWD:/app" -w /app python_dbc_reader bash -c 'flake8 . --count --max-complexity=11 --max-line-length=404 --statistics && coverage run -m unittest tests && coverage report -m'
```


## DBF specification

### What APIs I tested?

- https://github.com/frankyxhl/dbfpy3
- https://github.com/AlertaDengue/PySUS

### Resources

- http://dbase.com/Knowledgebase/INT/db7_file_fmt.htm
- https://wiki.dbfmanager.com/dbf-structure
- https://epics.anl.gov/EpicsDocumentation/AppDevManuals/AppDevGuide/3.12BookFiles/chapter12.html
- https://www.dbf2002.com/dbf-file-format.html

### Summary

| Byte	| Contents	    | Description |
| ------| --------------| ----------- |
| 0     | 1 byte	    | Valid dBASE for Windows table file, bits 0-2 indicate version number: 3 for dBASE Level 5, 4 for dBASE Level 7. Bit 3 and bit 7 indicate presence of a dBASE IV or dBASE for Windows memo file; bits 4-6 indicate the presence of a dBASE IV SQL table; bit 7 indicates the presence of any .DBT memo file (either a dBASE III PLUS type or a dBASE IV or dBASE for Windows memo file). |
| 1-3	| 3 bytes	    | Date of last update; in YYMMDD format.  Each byte contains the number as a binary.  YY is added to a base of 1900 decimal to determine the actual year. Therefore, YY has possible values from 0x00-0xFF, which allows for a range from 1900-2155. |
| 4-7	| 32-bit number	| Number of records in the table. (Least significant byte first.) |
| 8-9	| 16-bit number	| Number of bytes in the header. (Least significant byte first.) |
| 10-11	| 16-bit number	| Number of bytes in the record. (Least significant byte first.) |
| 12-13	| 2 bytes	    | Reserved; filled with zeros. |
| 14	| 1 byte	    | Flag indicating incomplete dBASE IV transaction. |
| 15	| 1 byte	    | dBASE IV encryption flag. |
| 16-27	| 12 bytes	    | Reserved for multi-user processing. |
| 28	| 1 byte	    | Production MDX flag; 0x01 if a production .MDX file exists for this table; 0x00 if no .MDX file exists. |
| 29	| 1 byte	    | Language driver ID. |
| 30-31	| 2 bytes	    | Reserved; filled with zeros. |
| 32-63	| 32 bytes	    | Language driver name. |
| 64-67	| 4 bytes	    | Reserved. |
| 68-n	| 48 bytes each | Field Descriptor Array (see 1.2). |
| n+1	| 1 byte	    | 0x0D stored as the Field Descriptor terminator. |
| n+2	| Complex       | Field Properties Structure. See below for calculations of size. |

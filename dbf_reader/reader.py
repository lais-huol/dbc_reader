#!/usr/bin/env python
from typing import Union, Dict, List
import codecs
from datetime import date
from io import RawIOBase, FileIO, SEEK_SET
from .definitions import TableDefinition, FieldDefinition


class Casts:
    def to_number(field: FieldDefinition, value: str) -> Union[float, int, None]:
        value = value.replace('\x00', '').lstrip()
        if value == '':
            return None
        if field.decimals > 0:
            return float(value)
        else:
            return int(value)

    def to_date(field: FieldDefinition, value: str) -> Union[date, None]:
        return date(int(value[:4]), int(value[4:6]), int(value[6:8]))

    def to_bool(field: FieldDefinition, value: str) -> Union[bool, None]:
        if value in ['T', 'F']:
            return value == 'T'
        return None

    def to_str(field: FieldDefinition, value: bytes) -> Union[str, None]:
        return value.rstrip()

    CAST_MAP = {
        'N': to_number,
        'D': to_date,
        'L': to_bool,
        'C': to_str,
    }


class DbfReader(RawIOBase):

    def __init__(self, file_object: Union[str, FileIO], encoding: str = 'iso-8859-1', table_definition: TableDefinition = None) -> None:
        # Check file object mode is read and binary
        _file_object = open(file_object, 'rb') if isinstance(file_object, str) else file_object

        if hasattr(_file_object, 'mode') and _file_object.mode != 'rb':
            raise IOError("File object need to be in binary readble mode ('rb')")

        # Check encoding exists
        print(encoding)
        codecs.lookup(encoding)

        self.file_object = _file_object
        self.encoding = encoding
        self.actual_record = 0
        self.file_size = None
        self.records = None
        self.last_update = None
        if table_definition is None:
            self.definition = TableDefinition(self, self.encoding)
        # else:
        #     self.definition = table_definition
        #     self.file_object.read(self.definition.headerlen)

    def __iter__(self) -> Dict[str, Union[str, float, int, date, bool]]:
        while self.actual_record < self.records:
            self.actual_record += 1
            deleted = self.read(1)
            if deleted != b' ':
                self.read(self.definition.record_size-1)
                continue
            result = {}
            for field in self.definition.fields:
                result[field.name] = self.get_field_value(field)
            yield result

    def get_field_value(self, field) -> Union[str, float, int, date, bool]:
        return Casts.CAST_MAP[field.type](field, self.read(field.size).decode(self.encoding))

    # INPUT/OUTPUT
    def close(self) -> None:
        if hasattr(self, 'file_object') and self.file_object is not None:
            return self.file_object.close()

    @property
    def closed(self) -> bool:
        return hasattr(self, 'file_object') and self.file_object is not None and self.file_object.closed

    def fileno(self) -> int:
        return self.file_object.fileno() if not self.closed else None

    def isatty(self) -> bool:
        return self.file_object.isatty()

    def seek(self, offset, whence=SEEK_SET) -> int:
        return self.file_object.seek(offset, whence)

    def seekable(self) -> bool:
        return self.file_object.seekable()

    def tell(self) -> int:
        return self.file_object.tell()

    def __del__(self) -> None:
        if hasattr(self, 'file_object') and self.file_object is not None:
            self.close()
            return self.file_object.__del__()

    # INPUT
    def readable(self) -> bool:
        return self.file_object.readable()

    def read(self, size: int) -> bytes:
        return self.file_object.read(size)

    def readline(self, *args) -> bytes:
        raise NotImplementedError()

    def readlines(self, *args) -> List[bytes]:
        raise NotImplementedError()

    def readall(self) -> bytes:
        raise NotImplementedError()

    def readinto(self, *args) -> int:
        raise NotImplementedError()

    # OUTPUT
    def writable(self) -> bool:
        return False

    def write(self, *args) -> int:
        raise NotImplementedError()

    def writelines(self, *args) -> None:
        raise NotImplementedError()

    def flush(self) -> None:
        raise NotImplementedError()

    def truncate(self, *args) -> int:
        raise NotImplementedError()

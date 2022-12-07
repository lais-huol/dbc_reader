import os
import sys
from pathlib import Path
import subprocess
from io import BytesIO
from dbf_reader import DbfReader
from dbf_reader.definitions import TableDefinition


class DbcReader(DbfReader):

    def __init__(self, file_object: str, encoding: str = 'iso-8859-1', table_definition: TableDefinition = None) -> None:
        _file_content = BytesIO(self._blast(file_object))
        super().__init__(file_object=_file_content, encoding=encoding, table_definition=table_definition)

    def _blast(self, file_object: str) -> BytesIO:
        if not os.path.exists(file_object):
            raise Exception(f"Arquivo '{file_object}' não encontrado.")

        _file_object = open(file_object, 'rb') if isinstance(file_object, str) else file_object

        if _file_object.mode != 'rb':
            raise IOError("File object need to be in binary readble mode ('rb')")

        blast_filename = 'blast-dbf.exe' if sys.platform == 'win32' else f'blast-dbf-{sys.platform}'
        blast = Path(__file__).resolve() / 'bin' / blast_filename
        command = f'{blast} < {_file_object}'

        result = b''
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while True:
            output = process.stdout.read()
            if output == '' and process.poll() is not None or output == b'':
                break
            if output:
                result += output.strip()

        return result

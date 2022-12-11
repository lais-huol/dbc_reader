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

    def _blast(self, filename: str) -> BytesIO:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Arquivo '{filename}' não encontrado.")

        blast_filename = 'blast-dbf.exe' if sys.platform == 'win32' else f'blast-dbf-{sys.platform}'
        blast = Path(__file__).parent.resolve() / 'bin' / blast_filename
        command = f'{blast} < {filename}'

        result = b''
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as process:
            while True:
                output = process.stdout.read()
                if output == b'':
                    break
                if output:
                    result += output.strip()
        return result

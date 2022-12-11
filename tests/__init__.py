import os
import unittest
import datetime
from dbc_reader import DbcReader
from dbf_reader.renderers import DbfDescriptionText


PATH_ROOT = os.path.dirname(os.path.abspath(__file__))


class TestDbfReader(unittest.TestCase):

    def test_file_not_exists(self):
        with self.assertRaises(FileNotFoundError):
            DbcReader("tests/data/filenotexsits.dbc")

    def test_read(self):
        with open("tests/data/EEAL0703.txt") as txt:
            with DbcReader("tests/data/EEAL0703.dbc") as dbc:
                self.assertIsNotNone(dbc.definition)
                self.assertEqual(DbfDescriptionText(dbc.definition).__str__(), txt.read())
                self.assertEqual(dbc.actual_record, 0)
                self.assertEqual(dbc.records, 1)
                self.assertEqual(dbc.last_update, datetime.date(2010, 3, 28))
                self.assertEqual(dbc.definition.reader, dbc)
                self.assertEqual(dbc.definition.encoding, 'iso-8859-1')
                self.assertEqual(dbc.definition.dbf_format, 3)
                self.assertEqual(dbc.definition.headerlen, 993)
                self.assertEqual(dbc.definition.numfields, 30)
                self.assertEqual(dbc.definition.record_size, 179)
                self.assertIsNotNone(dbc.definition.fields)
                self.assertEqual(dbc.definition.terminator, b'\r')

    def test_iterate(self):
        with DbcReader("tests/data/EEAL0703.dbc") as dbc:
            [row for row in dbc]
            self.assertEqual(dbc.actual_record, dbc.records)

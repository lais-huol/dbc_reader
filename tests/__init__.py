import os
import unittest
import datetime
from dbc_reader import DbcReader
from dbf_reader.renderers import DbfDescriptionText


PATH_ROOT = os.path.dirname(os.path.abspath(__file__))


class TestDbfReader(unittest.TestCase):

    def test_read(self):
        with DbcReader("tests/data/EEAL0703.dbc") as dbc:
            print(DbfDescriptionText(dbc))
            self.assertEqual(dbc.actual_record, 0)
            self.assertEqual(dbc.file_size, 9286)
            self.assertEqual(dbc.records, 14)
            self.assertEqual(dbc.last_update, datetime.date(1905, 7, 13))
            self.assertIsNotNone(dbc.definition)
            self.assertEqual(dbc.definition.reader, dbc)
            self.assertEqual(dbc.definition.encoding, 'iso-8859-1')
            self.assertEqual(dbc.definition.dbf_format, 3)
            self.assertEqual(dbc.definition.headerlen, 1025)
            self.assertEqual(dbc.definition.numfields, 31)
            self.assertEqual(dbc.definition.record_size, 590)
            self.assertIsNotNone(dbc.definition.fields)
            self.assertEqual(dbc.definition.terminator, b'\r')

    def test_iterate(self):
        with DbcReader("tests/data/EEAL0703.dbc", 'rb') as dbc:
            [row for row in dbc]
            self.assertEqual(dbc.actual_record, dbc.records)

#!/usr/bin/env python
from .definitions import TableDefinition, FieldDefinition


class DbfDescriptionText:
    def __init__(self, definition: TableDefinition) -> None:
        self.definition = definition

    def __str__(self) -> str:
        result = ''
        result += f"""
FILE DEFINITION
filename: {self.definition.reader.file_object.name}
header's length:   {self.definition.headerlen}
number of fields:  {self.definition.numfields}
line size:         {self.definition.record_size}

"""
        result += "FIELDS\n  (order,         name, type, size, decimals)\n"
        for field in self.definition.fields:
            result += f"   {field.order:>5}, {field.name:<12}, {field.type:>4}, {field.size:>4}, {field.decimals:>8}\n"
        return result


class DbfDescriptionMarkdown:
    def __init__(self, definition: TableDefinition) -> None:
        self.definition = definition

    def __str__(self) -> str:
        result = f"""
### File {self.definition.reader.file_object.name} description

| info              | value   |
| ----------------- | ------- |
| header's length   | {self.definition.headerlen:>7} |
| number of fields  | {self.definition.numfields:>7} |
| line size         | {self.definition.record_size:>7} |

### Fields

| order | name         | type | size | decimals |
| ----- | ------------ | ---- | ---- | -------- |
"""
        for field in self.definition.fields:
            result += f"| {field.order:>5} | {field.name:<12} | {field.type:>4} | {field.size:>4} | {field.decimals:>8} |\n"
        return result


class DbfDescriptionPostgresDDL:
    def __init__(self, definition: TableDefinition) -> None:
        self.definition = definition

    def __str__(self) -> str:
        schema = 'schemaname'
        tablename = 'tablename'
        fields = ",\n".join([DbfDescriptionPostgresDDL.pg_field_definition(field) for field in self.definition.fields])
        return f"CREATE SCHEMA IF NOT EXISTS {schema};\n\nCREATE TABLE IF NOT EXISTS {schema}.{tablename} (\n{fields}\n);"

    @staticmethod
    def pg_field_type(field: FieldDefinition) -> str:
        if field.type == "N":
            if field.decimals > 0:
                return f"numeric({field.size}, {field.decimals})"
            else:
                if field.size <= 4:
                    return "smallint"
                elif field.size <= 9:
                    return "integer"
                elif field.size <= 18:
                    return "bigint"
                else:
                    raise ValueError(f"Field {field.name} is too large ({field.size}).")
        elif field.type == 'D':
            return "date"
        elif field.type == 'L':
            return "boolean"
        elif field.type == 'C':
            return f"character varying({field.size})"

    @staticmethod
    def pg_field_definition(field: FieldDefinition) -> str:
        pg_type = DbfDescriptionPostgresDDL.pg_field_type(field)
        return f'  {field.name.lower():<12} {pg_type:<21} NULL'

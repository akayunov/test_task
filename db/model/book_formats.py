from sqlalchemy import Table, Column, Integer, String

user = Table(
    "book_formats",
    metadata_obj,
    Column("book_id", Integer, primary_key=True),
    Column("format_name", String(255), nullable=False),
    Column("creation_date", Integer(255), nullable=False),
    Column("path", String(255), nullable=False),
    Index('format_name_idx', 'format_name'),
)
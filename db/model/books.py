from sqlalchemy import Table, Column, Integer, String

user = Table(
    "books",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("creation_date", Integer(255), nullable=False),
    Index('book_name_idx', 'book_name'),
)
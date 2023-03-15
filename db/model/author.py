from sqlalchemy import Table, Column, Integer, String, Index

user = Table(
    "author",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String(255), nullable=False),
    Column("second_name", String(255), nullable=False),
    Column("email_address", String(60)),
    Index('author_first_name_idx', 'first_name'),
    Index('author_second_name_idx', 'second_name'),

)
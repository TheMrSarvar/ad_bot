from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, BIGINT, Text, Boolean

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('chat_id', BIGINT),
    Column('added_date', DateTime, default=datetime.utcnow),
    Column('language', String, default='uzbek'),
    Column('count_ads', BIGINT, default=0),
)

chats = Table(
    'chats',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('chat_id', BIGINT),
    Column('username', String),
    Column('message', Text),
)

adding = Table(
    "adding",
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('chat_id', BIGINT),
    Column("text", Text),
    Column("paid", Boolean, default=False),
    Column('confirm', Boolean, default=False),
    Column("photo_id", String),
    Column("years", Text),
    Column("probeg", Text),
    Column("status", Text),
    Column("amenities", Text),
    Column("condition", Text),
    Column("fuel", Text),
    Column("payment", Text),
    Column("phone_number", Text),
    Column("address", Text),
    Column("subject_photo", Text),
    Column("color", Text),
    Column("money", Text),
    Column("numeration_files", Text),
    Column("rejected", Boolean, default=False),
    Column("date_added", DateTime, default=datetime.utcnow),
    Column("language", Text),
)

admins = Table(
    'admins',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('chat_id', BIGINT),
    Column("name", String),
    Column("superadmin", Boolean, default=False),
)

reklama = Table(
    "reklama",
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('ad_id', String),
    Column("caption", Text),
    Column("superadmin", Boolean, default=False),
)

card = Table(
    "card",
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('card_id', BIGINT),
    Column("amount_som", BIGINT)
)

message_adding = Table(
    "message_adding",
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('chat_id', BIGINT),
    Column('message', Text),
    Column("message_id", BIGINT),
    Column("ad_id", BIGINT)
)

paid_message = Table(
    "paid_message",
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('chat_id', BIGINT),
    Column('num', BIGINT),
    Column('message', Text),
    Column("admin_id", BIGINT),
    Column("message_id", BIGINT),
    Column("type", Text),
)

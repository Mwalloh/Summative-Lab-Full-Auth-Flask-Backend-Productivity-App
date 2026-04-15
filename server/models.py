from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from marshmallow import Schema, fields, ValidationError, validates_schema, validate, post_load
from pprint import pprint

metadata = MetaData(
    naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)
db = SQLAlchemy(metadata=metadata)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    
    journal_entries = db.relationship('JournalEntry', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'
    
class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String(validate=validate.Range(3, 80), required=True)
    password = fields.String(validate=validate.Range(8, ), required=True)
    
    @post_load
    def make_entry(self, data, **kwargs):
        return User(**data)
    
    
class JournalEntry(db.Model):
    __tablename__ = 'journalEntries'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    content = db.Column(db.String(50), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship('User', back_populates='journal_entries')
    
    def __repr__(self):
        return f'<User {self.title}, description: {self.content}>'
    
class JournalEntrySchema(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    content = fields.String(required=True)
    
    @validates_schema
    def check_entry_duplicate(self, data, **kwargs):
        title = data.get('title')
        content = data.get('content')

        # Example duplicate check (you must import your model)
        existing = JournalEntry.query.filter_by(
            title=title,
            content=content
        ).first()

        if existing:
            raise ValidationError(
                "Journal entry already exists",
                field_name="title"
            )
            
    @post_load
    def make_entry(self, data, **kwargs):
        return JournalEntry(**data)
    

from myflask.exts import db
from core.database import Model


class User(Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, doc='ID')
    username = db.Column(db.String(32), nullable=False, unique=True, doc='用户名')

    def __repr__(self):
        return f'<User({self.id!r})>'

    def __str__(self):
        return f'{self.id}-{self.username}'

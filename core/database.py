from functools import wraps
import itertools
import datetime
import enum
from decimal import Decimal

from sqlalchemy.orm import relationship
from sqlalchemy.orm.query import Query

from myflask.exts import db
from core.helpers import underscore, camelize

# Alias common SQLAlchemy names
Column = db.Column


def paginate(qexp_or_model, page=1, page_size=10, order_by='id', entity=None):
    qexp = qexp_or_model
    if hasattr(qexp, 'query'):
        qexp = qexp.query
    assert isinstance(qexp, Query)

    # only flask_sqlalchemy
    if not entity:
        entity = qexp._primary_entity.entity_zero.entity

    if order_by:
        if not isinstance(order_by, list):
            order_by = [order_by]

        order_by = [i for i in order_by if i]  # exclude ''
        order_by = [f'-{underscore(i[1:])}' if i.startswith('-') else underscore(i) for i in order_by]

        columns = {i.name for i in entity.__table__.columns}
        diff = {c.lstrip('-') for c in order_by} - columns
        if diff:
            raise Exception(f'columns {diff} not exist in {entity} model')

        order_exp = []
        for column in order_by:
            if column.startswith('-'):
                order_exp.append(getattr(entity, underscore(column.lstrip('-'))).desc())
            else:
                order_exp.append(getattr(entity, underscore(column)))
        qexp = qexp.order_by(*order_exp)
    data = qexp.paginate(page, page_size, error_out=False)
    return {
        'items': data.items,
        'total': data.total
    }


def data_paginate(iterable, page=1, page_size=10, order_by='id'):
    if not iterable:
        return {
            'items': [],
            'total': 0
        }
    is_reverse = True if '-' in order_by else False
    iterable.sort(key=lambda x: getattr(x, underscore(order_by.strip('-'))), reverse=is_reverse)

    page = page - 1 if page > 0 else 0
    if page_size <= 0:
        page_size = 10
    items = itertools.islice(iterable[page*page_size:], page_size)

    return {
        'items': list(items),
        'total': len(iterable)
    }


def df_paginate(df, page=1, page_size=10, order_by=[]):
    if order_by:
        direction = [not d.startswith('-') for d in order_by]
        order_by = [d.strip('-') for d in order_by]
        order_by = [underscore(i) for i in order_by]
        df = df.sort_values(order_by, ascending=direction)
    total = df.shape[0]
    df = df.iloc[((page - 1) * page_size):(page * page_size)]
    df.columns = [camelize(i) for i in df.columns]
    items = df.to_dict(orient='records')

    return {
        'items': items,
        'total': total,
    }


class __CRUDMixin(object):
    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save(commit=commit)

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            self.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and self.commit()

    @classmethod
    def exists(cls, id):
        rcd = cls.query.get(id)
        return True and rcd

    @classmethod
    def upsert(cls, constraint, commit=True, **kwargs):
        q = cls.query
        rcd = None
        if isinstance(constraint, str):
            rcd = cls.query.filter(
                getattr(cls, constraint) == kwargs.get(constraint)).first()
        elif isinstance(constraint, list) or isinstance(constraint, tuple):
            for c in constraint:
                q = q.filter(getattr(cls, c) == kwargs.get(c))
            rcd = q.first()

        if not rcd:
            instance = cls(**kwargs)
            return instance.save(commit=commit)
        else:
            for k, v in kwargs.items():
                setattr(rcd, k, v)
            return rcd.save(commit=commit)

    @classmethod
    def bulk_save(cls, rcds, commit=True):
        assert isinstance(rcds, list)
        db.session.add_all(rcds)
        if commit:
            cls.commit()
        return True

    @classmethod
    def bulk_delete(cls, rcds, commit=True):
        assert isinstance(rcds, list)
        for rcd in rcds:
            db.session.delete(rcd)
        if commit:
            cls.commit()
        return True

    @classmethod
    def commit(cls):
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def flush(self):
        db.session.flush()

    def to_dict(self):
        result = {}
        # 目前未处理password二进制值的情况
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, datetime.date):
                value = value.strftime('%Y-%m-%d')
            elif isinstance(value, enum.Enum):
                value = value.name
            elif isinstance(value, Decimal):
                value = str(value)
            result.update({c.name: value})
        return result

    def get_foreign_keys(self):
        return [e.target_fullname.replace('.', '_') for e in self.__table__.foreign_keys]


class Model(__CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True


def reference_col(tablename, nullable=False, pk_name='id', ondelete='CASCADE', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(db.ForeignKey(f'{tablename}.{pk_name}', ondelete=ondelete),
                     nullable=nullable, **kwargs)


def atomic(session=db.session, nested=False):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            with session.no_autoflush:
                if session.autocommit is True and nested is False:
                    session.begin()  # start a transaction

                try:
                    with session.begin_nested():
                        resp = func(*args, **kwargs)
                    if not nested:
                        session.commit()  # transaction finished
                except Exception as e:
                    if not nested:
                        session.rollback()
                        session.remove()
                    raise e
                return resp
        return inner
    return wrapper


__all__ = [
    'db',
    'Model',
    'Column',
    'relationship',
    'reference_col',
    'atomic',
    'paginate',
]

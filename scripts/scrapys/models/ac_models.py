# -*- encoding: utf-8 -*-
import datetime, json
from typing import Text
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base



class DirectiveJsonEncoder(json.JSONEncoder):
    """
        应对datetime.datetime() 对象的序列化,参考:
        https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class Base(object):
    id = sa.Column(sa.Integer,primary_key=True)
    created = sa.Column(
        sa.DateTime,
        default=datetime.datetime.now,
        nullable=False,
        index=True,
    )
    updated = sa.Column(
        sa.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_json(self):
        return json.dumps(self.as_dict(), ensure_ascii=False, cls=DirectiveJsonEncoder)


DeclarativeBase = declarative_base(cls=Base)

class ApiInfosModel(DeclarativeBase):
    __tablename__="ac_info_set"

    platform = sa.Column(sa.String(64),nullable=False,comment="所属平台")
    is_free =  sa.Column(sa.Boolean,nullable=False,comment="是否免费")
    api_type = sa.Column(sa.String(64),nullable=False,comment="api所属类别")
    api_name = sa.Column(sa.String(64),nullable=False,comment="api名称")
    api_icon = sa.Column(sa.String(128),nullable=False,comment="api对应的icon")
    api_url = sa.Column(sa.String(64),nullable=False,comment="api对应的url")
    clicked = sa.Column(sa.Integer,nullable=False,comment="点击次数")
    expire_time = sa.Column(sa.DateTime,nullable=False,comment="到期时间")
    api_price =sa.Column(sa.Float,nullable=False,comment="api价格")
    api_price_unit = sa.Column(sa.String(64),nullable=False,comment="api价格单位")
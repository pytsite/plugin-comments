"""PytSite Comments Plugin Models
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Iterable as _Iterable
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from datetime import datetime as _datetime
from pytsite import util as _util, lang as _lang, router as _router
from plugins import auth as _auth, http_api as _http_api


class AbstractComment(_ABC):
    @property
    def author(self) -> _auth.model.AbstractUser:
        raise NotImplementedError("Not implemented yet")

    @property
    def body(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def children(self):
        """
        :rtype: _Iterable[AbstractComment]
        """
        raise NotImplementedError("Not implemented yet")

    @property
    def created(self) -> _datetime:
        raise NotImplementedError("Not implemented yet")

    @property
    def depth(self) -> int:
        raise NotImplementedError("Not implemented yet")

    @property
    def is_reply(self) -> bool:
        return bool(self.parent_uid)

    @property
    def parent_uid(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def permissions(self) -> dict:
        raise NotImplementedError("Not implemented yet")

    @property
    def publish_time(self) -> _datetime:
        raise NotImplementedError("Not implemented yet")

    @property
    def thread_uid(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def uid(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def url(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def status(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @_abstractmethod
    def delete(self):
        raise NotImplementedError()

    def as_jsonable(self) -> dict:
        r = {
            'author': {
                'uid': self.author.uid,
                'nickname': self.author.nickname,
                'name': self.author.first_last_name,
                'picture_url': self.author.picture.get_url(width=50, height=50),
            },
            'depth': self.depth,
            'parent_uid': self.parent_uid,
            'permissions': self.permissions,
            'publish_time': {
                'w3c': _util.w3c_datetime_str(self.publish_time),
                'pretty_date': _lang.pretty_date(self.publish_time),
                'pretty_date_time': _lang.pretty_date_time(self.publish_time),
                'ago': _lang.time_ago(self.publish_time),
            },
            'children': [c.as_jsonable() for c in self.children],
            'status': self.status,
            'thread_uid': self.thread_uid,
            'uid': self.uid,
            'urls': {
                'delete': _http_api.url('comments@delete_comment', {'uid': self.uid}),
                'report': _http_api.url('comments@report_comment', {'uid': self.uid}),
                'view': _router.url(self.thread_uid, fragment='pytsite-comment-{}'.format(self.uid)),
            },
        }

        if self.status == 'published':
            r.update({
                'body': self.body
            })

        return r

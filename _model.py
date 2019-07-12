"""PytSite Comments Plugin Models
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Iterable
from abc import ABC, abstractmethod
from datetime import datetime
from pytsite import util, lang, router
from plugins import auth, http_api


class AbstractComment(ABC):
    @property
    def author(self) -> auth.model.AbstractUser:
        raise NotImplementedError("Not implemented yet")

    @property
    def body(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def children(self):
        """
        :rtype: Iterable[AbstractComment]
        """
        raise NotImplementedError("Not implemented yet")

    @property
    def created(self) -> datetime:
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
    def publish_time(self) -> datetime:
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

    @abstractmethod
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
                'w3c': util.w3c_datetime_str(self.publish_time),
                'pretty_date': lang.pretty_date(self.publish_time),
                'pretty_date_time': lang.pretty_date_time(self.publish_time),
                'ago': lang.time_ago(self.publish_time),
            },
            'children': [c.as_jsonable() for c in self.children],
            'status': self.status,
            'thread_uid': self.thread_uid,
            'uid': self.uid,
            'urls': {
                'delete': http_api.url('comments@delete_comment', {'uid': self.uid}),
                'report': http_api.url('comments@report_comment', {'uid': self.uid}),
                'view': router.url(self.thread_uid, fragment='pytsite-comment-{}'.format(self.uid)),
            },
        }

        if self.status == 'published':
            r.update({
                'body': self.body
            })

        return r

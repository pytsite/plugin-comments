"""PytSite Comments Plugin Abstract Driver
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Iterable
from abc import ABC, abstractmethod
from plugins import widget, auth
from . import _model


class Abstract(ABC):
    """Abstract Comments Driver
    """

    @abstractmethod
    def get_name(self) -> str:
        """Get driver's name
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get driver's description
        """
        pass

    @abstractmethod
    def create_comment(self, thread_uid: str, body: str, author: auth.model.AbstractUser,
                       status: str = 'published', parent_uid: str = None) -> _model.AbstractComment:
        """Create new comment
        """
        pass

    @abstractmethod
    def get_widget(self, widget_uid: str, thread_uid: str) -> widget.Abstract:
        """Get comments widget
        """
        pass

    @abstractmethod
    def get_comments(self, thread_uid: str, limit: int = 0, skip: int = 0) -> Iterable[_model.AbstractComment]:
        """Get comments
        """
        pass

    @abstractmethod
    def get_comment(self, uid: str) -> _model.AbstractComment:
        """Get single comment by UID
        """
        pass

    @abstractmethod
    def get_comments_count(self, thread_uid: str) -> int:
        """Get comments count for particular thread
        """
        pass

    @abstractmethod
    def delete_comment(self, uid: str):
        """Mark comment as deleted
        """
        pass

    @abstractmethod
    def delete_thread(self, thread_uid: str):
        """Physically remove comments for particular thread
        """
        pass

    @abstractmethod
    def get_permissions(self, user: auth.model.AbstractUser = None) -> dict:
        """Get permissions definition for user
        """
        pass

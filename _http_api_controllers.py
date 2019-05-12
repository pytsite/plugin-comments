"""PytSite Comments Plugin HTTP API
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from base64 import b32decode as _b32decode
from pytsite import lang as _lang, routing as _routing, events as _events, util as _util
from plugins import auth as _auth
from . import _api, _error


class GetSettings(_routing.Controller):
    """Get comments settings
    """

    def exec(self) -> dict:
        return {
            'min_body_length': _api.get_comment_min_body_length(),
            'max_body_length': _api.get_comment_max_body_length(),
            'max_depth': _api.get_comment_max_depth(),
            'statuses': _api.get_comment_statuses(),
            'permissions': _api.get_permissions(_auth.get_current_user(), self.arg('driver')),
        }


class PostComment(_routing.Controller):
    """Create new comment
    """

    def exec(self) -> dict:
        thread_uid = _util.url_unquote(_b32decode(self.arg('thread_uid')))

        body = self.arg('body', '').strip()
        if not body:
            raise self.server_error(_lang.t('comments@comment_body_cannot_be_empty'))

        status = 'published'
        parent_uid = self.arg('parent_uid')
        comment = _api.create_comment(thread_uid, body, _auth.get_current_user(), status, parent_uid,
                                      self.arg('driver'))

        return comment.as_jsonable()


class GetComment(_routing.Controller):
    """Get single comment
    """

    def exec(self) -> dict:
        return _api.get_comment(self.arg('uid'), self.arg('driver')).as_jsonable()


class GetComments(_routing.Controller):
    """Get comments for particular thread
    """

    def exec(self) -> dict:
        limit = abs(int(self.arg('limit', 0)))
        skip = abs(int(self.arg('skip', 0)))
        thread_uid = _util.url_unquote(_b32decode(self.arg('thread_uid')))
        comments = list(_api.get_driver().get_comments(thread_uid, limit, skip))

        return {
            'items': [comment.as_jsonable() for comment in comments],
        }


class DeleteComment(_routing.Controller):
    """Delete comment
    """

    def exec(self) -> dict:

        try:
            _api.get_driver().delete_comment(self.arg('uid'))
            return {'status': True}

        except _error.CommentNotExist as e:
            raise self.not_found(str(e))


class PostReport(_routing.Controller):
    """Report comment
    """

    def exec(self) -> dict:
        _events.fire('comments@report', uid=self.arg('uid'))

        return {'status': True}

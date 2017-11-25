"""PytSite Comments Plugin HTTP API
"""
from pytsite import lang as _lang, routing as _routing, events as _events
from plugins import auth as _auth
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class GetSettings(_routing.Controller):
    """Get comments settings
    """

    def exec(self) -> dict:
        return {
            'body_min_length': _api.get_comment_body_min_length(),
            'body_max_length': _api.get_comment_body_max_length(),
            'max_depth': _api.get_comment_max_depth(),
            'statuses': _api.get_comment_statuses(),
            'permissions': _api.get_permissions(_auth.get_current_user(), self.arg('driver')),
        }


class PostComment(_routing.Controller):
    """Create new comment
    """

    def exec(self) -> dict:

        thread_uid = self.arg('thread_uid')
        if not thread_uid:
            raise self.server_error('Thread UID is not specified')

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
        thread_uid = self.arg('thread_uid')
        if not thread_uid:
            raise RuntimeError('Thread UID is not specified')

        limit = abs(int(self.arg('limit', 0)))
        skip = abs(int(self.arg('skip', 0)))
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
        _events.fire('comments.report', uid=self.arg('uid'))

        return {'status': True}

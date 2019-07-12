"""PytSite Comments Plugin API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Dict as Dict, Iterable, Mapping
from frozendict import frozendict
from base64 import b32encode
from pytsite import router, reg, lang, cache, mail, tpl, events, util
from plugins import widget, auth
from . import _driver, _error, _model

_default_driver = None  # type: _driver.Abstract
_drivers = {}  # type: Dict[str, _driver.Abstract]
_comments_count = cache.create_pool('comments.count')

COMMENT_STATUS_PUBLISHED = 'published'
COMMENT_STATUS_WAITING = 'waiting'
COMMENT_STATUS_SPAM = 'spam'
COMMENT_STATUS_DELETED = 'deleted'

_COMMENT_STATUSES = [
    COMMENT_STATUS_PUBLISHED,
    COMMENT_STATUS_WAITING,
    COMMENT_STATUS_SPAM,
    COMMENT_STATUS_DELETED,
]


def register_driver(driver: _driver.Abstract):
    """Register a comments driver
    """
    global _drivers

    if not isinstance(driver, _driver.Abstract):
        raise TypeError("Instance of 'plugins.comments.driver.Abstract' expected.")

    driver_name = driver.get_name()

    if driver_name in _drivers:
        raise _error.DriverAlreadyRegistered("Driver '{}' is already registered".format(driver_name))

    _drivers[driver_name] = driver

    # Set default driver if it is not already set
    global _default_driver
    if not _default_driver:
        _default_driver = driver


def get_driver(name: str = None) -> _driver.Abstract:
    """Get driver instance.
    """
    if not _default_driver:
        raise _error.NoDriversRegistered('There is no comment drivers registered')

    if not name:
        return _drivers.get(reg.get('comments.driver', ''), _default_driver)
    elif name not in _drivers:
        raise _error.DriverNotRegistered("Driver '{}' is not registered".format(name))

    return _drivers[name]


def set_default_driver(name: str):
    """Set default driver.
    """
    global _default_driver

    _default_driver = get_driver(name)


def get_drivers() -> Mapping[str, _driver.Abstract]:
    """Get all registered drivers
    """
    return frozendict(_drivers)


def get_comment_statuses() -> Mapping:
    """Get valid comment statuses.
    """
    return {s: lang.t('comments@status_{}'.format(s)) for s in _COMMENT_STATUSES}


def get_comment_max_depth() -> int:
    """Get comment's max depth.
    """
    return int(reg.get('comments.max_comment_depth', 4))


def get_comment_min_body_length() -> int:
    """Get comment's body minimum length.
    """
    return int(reg.get('comments.min_comment_length', 2))


def get_comment_max_body_length() -> int:
    """Get comment's body maximum length.
    """
    return int(reg.get('comments.max_comment_length', 2048))


def get_widget(widget_uid: str = 'comments', thread_uid: str = None, driver_name: str = None) -> widget.Abstract:
    """Get comments widget.
    """
    if not thread_uid:
        thread_uid = util.url_quote(b32encode(router.current_path().encode('utf-8')).decode('ascii'))

    return get_driver(driver_name).get_widget(widget_uid, thread_uid)


def create_comment(thread_id: str, body: str, author: auth.model.AbstractUser, status: str = 'published',
                   parent_uid: str = None, driver_name: str = None) -> _model.AbstractComment:
    """Create a new comment
    """
    # Check min length
    if len(body) < get_comment_min_body_length():
        raise _error.CommentTooShort(lang.t('comments@error_body_too_short'))

    # Check max length
    if len(body) > get_comment_max_body_length():
        raise _error.CommentTooLong(lang.t('comments@error_body_too_long'))

    # Check status
    if status not in get_comment_statuses():
        raise _error.InvalidCommentStatus("'{}' is not a valid comment's status.".format(status))

    # Load driver
    driver = get_driver(driver_name)

    # Create comment
    comment = driver.create_comment(thread_id, body, author, status, parent_uid)
    events.fire('comments@create_comment', comment=comment)

    # Send email notification about reply
    if reg.get('comments.email_notify', True) and comment.is_reply:
        parent_comment = get_comment(comment.parent_uid)
        if comment.author != parent_comment.author:
            tpl_name = 'comments@mail/{}/reply'.format(lang.get_current())
            m_subject = lang.t('comments@mail_subject_new_reply')
            m_body = tpl.render(tpl_name, {
                'reply': comment,
                'comment': get_comment(comment.parent_uid, driver_name)
            })
            m_from = '{} <{}>'.format(author.first_last_name, mail.mail_from()[1])

            mail.Message(parent_comment.author.login, m_subject, m_body, m_from).send()

    return comment


def get_comment(uid: str, driver_name: str = None) -> _model.AbstractComment:
    """Get single comment by UID.
    """
    return get_driver(driver_name).get_comment(uid)


def get_comments(thread_id: str, limit: int = 0, skip: int = 0, status: str = 'published', driver_name: str = None) \
        -> Iterable[_model.AbstractComment]:
    """Get comments for a thread.
    """
    return get_driver(driver_name).get_comments(thread_id, limit, skip, status)


def delete_thread(thread_uid: str, driver_name: str = None):
    """Delete all comments of the thread
    """
    get_driver(driver_name).delete_thread(thread_uid)


def get_comments_count(thread_uid: str, driver_name: str = None) -> int:
    """Get comments count of the thread
    """
    c_key = '{}_{}'.format(thread_uid, driver_name)

    if _comments_count.has(c_key):
        return _comments_count.get(c_key)

    count = get_driver(driver_name).get_comments_count(thread_uid)
    _comments_count.put(c_key, count, 300)

    return count


def get_all_comments_count(thread_id: str):
    """Get comments count of the thread, all drivers
    """
    count = 0
    for driver_name in _drivers:
        count += get_comments_count(thread_id, driver_name)

    return count


def get_permissions(user: auth.model.AbstractUser = None, driver_name: str = None) -> dict:
    """Get permissions definition for user
    """
    if not user:
        user = auth.get_current_user()

    return get_driver(driver_name).get_permissions(user)

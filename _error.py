"""PytSite Comments Plugin Errors
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class DriverAlreadyRegistered(Exception):
    pass


class DriverNotRegistered(Exception):
    pass


class NoDriversRegistered(Exception):
    pass


class InvalidCommentStatus(Exception):
    pass


class CommentNotExist(Exception):
    pass


class CommentTooShort(Exception):
    pass


class CommentTooLong(Exception):
    pass

"""PytSite Comments Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _driver as driver, _error as error, _model as model
from ._api import COMMENT_STATUS_PUBLISHED, COMMENT_STATUS_WAITING, COMMENT_STATUS_SPAM, COMMENT_STATUS_DELETED
from ._api import register_driver, get_driver, get_widget, get_comments_count, get_all_comments_count, \
    get_drivers, create_comment, get_comment_statuses, get_comment_max_depth, get_comment_min_body_length, \
    get_comment, get_comment_max_body_length, get_comments, get_permissions, delete_thread, set_default_driver
from ._model import AbstractComment


def plugin_load():
    from plugins import permissions

    # Permissions
    permissions.define_group('comments', 'comments@comments')


def plugin_load_wsgi():
    from plugins import http_api, settings
    from . import _http_api_controllers, _settings_form

    # Settings
    settings.define('comments', _settings_form.Form, 'comments@comments', 'fa fas fa-comments', 'dev')

    # HTTP API
    http_api.handle('GET', 'comments/settings', _http_api_controllers.GetSettings, 'comments@get_settings')
    http_api.handle('GET', 'comments/comments/<thread_uid>', _http_api_controllers.GetComments, 'comments@get_comments')
    http_api.handle('POST', 'comments/comment/<thread_uid>', _http_api_controllers.PostComment, 'comments@post_comment')
    http_api.handle('GET', 'comments/comment/<uid>', _http_api_controllers.GetComment, 'comments@get_comment')
    http_api.handle('DELETE', 'comments/comment/<uid>', _http_api_controllers.DeleteComment, 'comments@delete_comment')
    http_api.handle('POST', 'comments/report/<uid>', _http_api_controllers.PostReport, 'comments@report_comment')

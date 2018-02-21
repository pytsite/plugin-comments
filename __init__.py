"""PytSite Comments Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _driver as driver, _error as error, _model as model
from ._api import register_driver, get_driver, get_widget, get_comments_count, get_all_comments_count, \
    get_drivers, create_comment, get_comment_statuses, get_comment_max_depth, get_comment_body_min_length, \
    get_comment, get_comment_body_max_length, get_comments, get_permissions, delete_thread, set_default_driver


def plugin_load():
    from pytsite import lang, tpl

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)


def plugin_load_wsgi():
    from plugins import permissions, settings, http_api
    from . import _http_api_controllers, _settings_form

    # Permissions
    permissions.define_group('comments', 'comments@comments')

    # Settings
    settings.define('comments', _settings_form.Form, 'comments@comments', 'fa fa-comments', 'dev')

    # HTTP API
    http_api.handle('GET', 'comments/settings', _http_api_controllers.GetSettings, 'comments@get_settings')
    http_api.handle('POST', 'comments/comment', _http_api_controllers.PostComment, 'comments@post_comment')
    http_api.handle('GET', 'comment/comment/<uid>', _http_api_controllers.GetComment, 'comments@get_comment')
    http_api.handle('GET', 'comments', _http_api_controllers.GetComments, 'comments@get_comments')
    http_api.handle('POST', 'comments/report/<uid>', _http_api_controllers.PostReport, 'comments@post_comment_report')
    http_api.handle('DELETE', 'comments/comment/<uid>', _http_api_controllers.DeleteComment, 'comments@delete_comment')

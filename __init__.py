"""PytSite Comments Package Init.
"""
# Public API
from . import _driver as driver, _error as error, _model as model
from ._api import register_driver, get_driver, get_widget, get_comments_count, get_all_comments_count, get_drivers, \
    create_comment, get_comment_statuses, get_comment_max_depth, get_comment_body_min_length, get_comment, \
    get_comment_body_max_length, get_comments, get_permissions, delete_thread


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    """Init wrapper.
    """
    from pytsite import lang, tpl, http_api, permissions, settings
    from . import _http_api, _settings_form

    # Resources
    lang.register_package(__name__, alias='comments')
    tpl.register_package(__name__, alias='comments')

    # Permissions
    permissions.define_group('comments', 'comments@comments')
    permissions.define_permission('comments.settings.manage', 'comments@manage_comments_settings', 'app')

    # Settings
    settings.define('comments', _settings_form.Form, 'comments@comments', 'fa fa-comments',
                    'comments.settings.manage')

    # HTTP API
    http_api.handle('GET', 'comments/settings', _http_api.get_settings, 'comments@get_settings')
    http_api.handle('GET', 'comments', _http_api.get_comments, 'comments@get_comments')
    http_api.handle('POST', 'comments/comment', _http_api.post_comment, 'comments@post_comment')
    http_api.handle('POST', 'comments/report/<uid>', _http_api.post_report, 'comments@post_report')
    http_api.handle('DELETE', 'comments/comment/<uid>', _http_api.delete_comment, 'comments@delete_comment')


_init()

"""PytSite Comments Plugin Settings Form
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import lang
from plugins import widget, settings
from . import _api


class Form(settings.Form):
    def _on_setup_widgets(self):
        """Hook
        """
        if not _api.get_drivers():
            self.remove_widget('action_submit')
            self.add_widget(widget.static.Text(
                uid='error_message',
                text=lang.t('comments@no_comments_driver_installed'),
            ))
            return

        self.add_widget(widget.select.Select(
            uid='setting_driver',
            weight=10,
            label=lang.t('comments@driver'),
            h_size='col-xs-12 col-sm-6 col-md-4 col-lg-3',
            append_none_item=False,
            required=True,
            items=[(k, d.get_description()) for k, d in sorted(_api.get_drivers().items())],
            default=_api.get_driver().get_name(),
        ))

        self.add_widget(widget.select.Select(
            uid='setting_max_comment_depth',
            weight=20,
            label=lang.t('comments@max_comment_depth'),
            h_size='col-xs-12 col-sm-3 col-md-2 col-lg-1',
            append_none_item=False,
            required=True,
            items=[(str(x), str(x)) for x in range(0, 11)],
            default=4,
        ))

        self.add_widget(widget.input.Integer(
            uid='setting_min_comment_length',
            weight=30,
            label=lang.t('comments@min_comment_length'),
            h_size='col-xs-12 col-sm-3 col-md-2 col-lg-1',
            default=2,
            required=True,
        ))

        self.add_widget(widget.input.Integer(
            uid='setting_max_comment_length',
            weight=40,
            label=lang.t('comments@max_comment_length'),
            h_size='col-xs-12 col-sm-3 col-md-2 col-lg-1',
            default=2048,
            required=True,
        ))

        super()._on_setup_widgets()

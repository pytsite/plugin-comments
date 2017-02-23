"""PytSite Comments Plugin Settings Form
"""
from pytsite import widget as _widget, lang as _lang, settings as _settings
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(_settings.Form):
    def _on_setup_widgets(self):
        """Hook.
        """
        self.add_widget(_widget.select.Select(
            uid='setting_driver',
            weight=10,
            label=_lang.t('comments@driver'),
            h_size='col-xs-12 col-sm-6 col-md-4 col-lg-3',
            append_none_item=False,
            required=True,
            items=[(k, d.get_description()) for k, d in sorted(_api.get_drivers().items())],
            default=_api.get_driver().get_name(),
        ))

        self.add_widget(_widget.select.Select(
            uid='setting_max_comment_depth',
            weight=20,
            label=_lang.t('comments@max_comment_depth'),
            h_size='col-xs-12 col-sm-3 col-md-2 col-lg-1',
            append_none_item=False,
            required=True,
            items=[(str(x), str(x)) for x in range(0, 11)],
            default=4,
        ))

        self.add_widget(_widget.input.Integer(
            uid='setting_min_comment_length',
            weight=30,
            label=_lang.t('comments@min_comment_length'),
            h_size='col-xs-12 col-sm-3 col-md-2 col-lg-1',
            default=2,
            required=True,
        ))

        self.add_widget(_widget.input.Integer(
            uid='setting_max_comment_length',
            weight=40,
            label=_lang.t('comments@max_comment_length'),
            h_size='col-xs-12 col-sm-3 col-md-2 col-lg-1',
            default=2048,
            required=True,
        ))

        super()._on_setup_widgets()

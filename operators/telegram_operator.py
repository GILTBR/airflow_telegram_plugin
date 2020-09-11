from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from airflow_telegram_plugin.hooks.telegram_hook import TelegramHook


class TelegramOperator(BaseOperator):
    # TODO Docstring

    ui_color = '#5E81AC'
    ui_fgcolor = '#ECEFF4'

    @apply_defaults
    def __init__(self, telegram_conn_id='telegram_conn_id', chat_id=None, message='', *args, **kwargs):
        # TODO Docstring
        super(TelegramOperator, self).__init__(*args, **kwargs)
        self.telegram_conn_id = telegram_conn_id
        self.chat_id = chat_id
        self.message = message

    def execute(self, context):
        # TODO Docstring
        hook = TelegramHook(telegram_conn_id=self.telegram_conn_id, chat_id=self.chat_id)
        self.log.info(f'Sending message: {self.message}')
        self.log.info(type(self.message))
        self.log.info(self.message.__dir__())
        self.log.info(isinstance(self.message, str))
        try:
            hook.send_message(message=self.message, parse_mode='Markdown')
        except AirflowException as e:
            self.log.exception(e)

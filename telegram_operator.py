from airflow.operators.bash_operator import BashOperator
from .telegram_hook import TelegramHook
from airflow.utils.decorators import apply_defaults


class TelegramOperator(BashOperator):
    # TODO Docstring
    @apply_defaults
    def __init__(self, telegram_conn_id='telegram_default', chat_id=None, message='', *args, **kwargs):
        # TODO Docstring
        super(TelegramOperator, self).__init__(*args, **kwargs)
        self.telegram_conn_id = telegram_conn_id
        self.chat_id = chat_id
        self.message = message

    def execute(self, context):
        # TODO Docstring
        hook = TelegramHook(telegram_conn_id=self.telegram_conn_id, chat_id=self.chat_id)
        hook.send_message(message=self.message)

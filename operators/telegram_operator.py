from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from airflow_telegram_plugin.hooks.telegram_hook import TelegramHook


class TelegramOperator(BaseOperator):
    """
    Send a message with Telegram using a bot client.
    """

    ui_color = '#5E81AC'
    ui_fgcolor = '#ECEFF4'

    @apply_defaults
    def __init__(self, telegram_conn_id='telegram_conn_id', token=None, chat_id=None, parse_mode=None, message='',
                 *args, **kwargs):
        """
        Takes both Telegram API token and Airflow connection that has a Telegram  API token in the password field.
        If both are provided, Telegram bot API token will be used.
        Takes both chat_id and Airflow connection_id with the chat_id in the host field.
        If both are provided, chat_id will be used.

        :param parse_mode: Parsing method for the message
        :type parse_mode: str
        :param telegram_conn_id: Airflow connection id
        :type telegram_conn_id: str
        :param token: Telegram API token
        :type token: str
        :param chat_id: Either a personal chat_id or a channel chat_id
        :type chat_id: int
        :param message: Message to send
        :type message: str
        """
        super(TelegramOperator, self).__init__(*args, **kwargs)
        self.parse_mode = parse_mode
        self.telegram_conn_id = telegram_conn_id
        self.token = token
        self.chat_id = chat_id
        self.message = message

    def execute(self, context):
        try:
            hook = TelegramHook(telegram_conn_id=self.telegram_conn_id, token=self.token, chat_id=self.chat_id)
        except AirflowException as e:
            self.log.exception(e)
            raise e
        else:
            hook.send_message(message=self.message, parse_mode=self.parse_mode)

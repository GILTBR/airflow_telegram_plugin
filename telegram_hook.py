import telebot
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook


class TelegramHook(BaseHook):
    # TODO Docstring

    def __init__(self, telegram_conn_id=None, token=None, chat_id=None, *args, **kwargs):
        # TODO Docstring
        super().__init__(*args, **kwargs)
        self.token = self._get_token(telegram_conn_id, token)
        self.chat_id = self._get_chat_id(telegram_conn_id, chat_id)

    def _get_token(self, telegram_conn_id, token):
        # TODO Docstring
        if token:
            return token

        elif telegram_conn_id:
            conn = self.get_connection(telegram_conn_id)

            if not conn.password:
                raise AirflowException('Token(password) is missing from telegram_conn_id')

            return conn.password
        else:
            raise AirflowException('Cannot get token: No valid Telegram token nor telegram_conn_id supplied.')

    def _get_chat_id(self, telegram_conn_id, chat_id):
        # TODO Docstring
        if chat_id:
            return chat_id

        if telegram_conn_id:
            conn = self.get_connection(telegram_conn_id)

            if not conn.host:
                raise AirflowException('Chat_id(host) is missing from telegram_conn_id')

            else:
                return conn.host

        else:
            raise AirflowException(
                "Cannot get chat_id: No valid chat_id nor telegram_conn_id with 'host' field was given")

    def send_message(self, message):
        # TODO Docstring
        telegram_client = telebot.TeleBot(token=self.token)
        telegram_client.send_message(chat_id=self.chat_id, text=message)

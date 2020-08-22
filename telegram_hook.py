from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowException
import telebot


class TelegramHook(BaseHook):

    def __init__(self, telegram_conn_id=None, chat_id=None, *args, **kwargs):

        super(TelegramHook, self).__init__(*args, **kwargs)
        self.token = self._get_token(telegram_conn_id)
        self.chat_id = self._get_chat_id(telegram_conn_id, chat_id)

    def _get_token(self, token, telegram_conn_id):
        if token:
            return token

        elif telegram_conn_id:
            conn = self.get_connection(telegram_conn_id)

            if not getattr(conn, 'password', None):
                raise AirflowException(f'Token(password) is missing Telegram connection')

            return conn.password
        else:
            raise AirflowException('Cannot get token: No valid Telegram token nor telegram_conn_id supplied.')

    def _get_chat_id(self, telegram_conn_id, chat_id):
        if chat_id:
            return chat_id

        if telegram_conn_id:
            conn = self.get_connection(telegram_conn_id)

            if not getattr(conn, 'host', None):
                raise AirflowException('write something')

            else:
                return conn.host

        else:
            raise AirflowException('write')

    def send_message(self, message):
        try:
            bot = telebot.TeleBot(token=self.token)
        except Exception as e:
            pass
        else:
            bot.send_message(chat_id=self.chat_id, text=message)

import telebot
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook


class TelegramHook(BaseHook):
    """
    Interact with Telegram and create a bot client, using the pyTelegramBotAPI library.
    """

    def __init__(self, telegram_conn_id=None, token=None, chat_id=None, *args, **kwargs):
        """
        Takes both Telegram bot API token and Airflow connection that has a Telegram bot API token.
        If both are provided, Telegram bot API token will be used

        :param telegram_conn_id:
        :type telegram_conn_id
        :param token: Telegram API token
        :type token: str
        :param chat_id:
        :type chat_id: str
        :return: Telegram bot object

        """
        super(TelegramHook, self).__init__(source=kwargs)
        self.token = self._get_token(telegram_conn_id, token)
        self.chat_id = self._get_chat_id(telegram_conn_id, chat_id)

    def _get_token(self, telegram_conn_id, token):
        # TODO Docstring
        """

        :param telegram_conn_id:
        :type telegram_conn_id: str
        :param token:
        :type token: str
        :return: Valid Telegram bot API token
        """
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
        """

        :param telegram_conn_id:
        :type telegram_conn_id:
        :param chat_id:
        :type chat_id:
        :return:
        """
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

    def send_message(self, message, parse_mode=None):
        # TODO Docstring
        telegram_client = telebot.TeleBot(token=self.token)
        self.log.info(f'Sending message: {message}')
        try:
            self.log.info(type(message))
            self.log.info(message.__dir__())
            self.log.info(isinstance(message, str))
            telegram_client.send_message(chat_id=self.chat_id, text=message, parse_mode=parse_mode)
        except AirflowException as e:
            self.log.exception(e)

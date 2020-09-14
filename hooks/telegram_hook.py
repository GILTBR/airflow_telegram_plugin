import telebot
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook


class TelegramHook(BaseHook):
    """
    Interact with Telegram and create a bot client, using the pyTelegramBotAPI library.

    Takes both Telegram API token and Airflow connection that has a Telegram  API token in the password field.
    If both are provided, Telegram bot API token will be used.

    Takes both chat_id and Airflow connection_id with the chat_id in the host field.
    If both are provided, chat_id will be used.

    :param telegram_conn_id: Airflow connection id
    :type telegram_conn_id: str
    :param token: Telegram API token
    :type token: str
    :param chat_id: Either a personal chat_id or a channel chat_id
    :type chat_id: int
    """

    def __init__(self, telegram_conn_id=None, token=None, chat_id=None, parse_mode=None, **kwargs):
        super(TelegramHook, self).__init__(source=kwargs)
        self.token = self._get_token(telegram_conn_id, token)
        self.chat_id = self._get_chat_id(telegram_conn_id, chat_id)
        self.parse_mode = parse_mode
        self.telegram_client = self._get_client(self.token, self.parse_mode)

    def _get_token(self, telegram_conn_id, token):
        """
        Returns valid API token. When both token and conn_id are given, token is used.

        :param telegram_conn_id: Airflow connection id.
        :type telegram_conn_id: str
        :param token: Telegram API token.
        :type token: str
        :return: Valid Telegram bot API token.
        :raise AirflowException:
        """
        if token:
            if isinstance(token, str):
                return token
            else:
                raise AirflowException('token must be of type string')
        elif telegram_conn_id:
            conn = self.get_connection(telegram_conn_id)
            if not conn.password:
                raise AirflowException(f"token is missing from {telegram_conn_id}'s 'password' field")
            else:
                return conn.password
        else:
            raise AirflowException('Cannot get token: No valid Telegram token nor telegram_conn_id supplied.')

    def _get_chat_id(self, telegram_conn_id, chat_id):
        """
        Returns valid chat_id.
        :param telegram_conn_id: Airflow connection id
        :type telegram_conn_id: str
        :param chat_id: Either a personal chat_id or a channel chat_id
        :type chat_id: int
        :return: Valid chat_id
        :param parse_mode: Parsing method for the message
        :type parse_mode: str
        """
        if chat_id:
            if isinstance(chat_id, int):
                return chat_id
            else:
                raise AirflowException('chat_id must be of type int')
        if telegram_conn_id:
            conn = self.get_connection(telegram_conn_id)
            if not conn.host:
                raise AirflowException(f"chat_id is missing from {telegram_conn_id}'s 'host' field")
            else:
                return conn.host
        else:
            raise AirflowException(
                "Cannot get chat_id: No valid chat_id nor telegram_conn_id with 'host' field was given")

    def _get_client(self, token, parse_mode):
        try:
            telegram_client = telebot.TeleBot(token=token, parse_mode=parse_mode)
        except AirflowException as e:
            self.log.exception(f'Error occurred while trying to create a telegram client: {e}')
            raise e
        else:
            return telegram_client

    def send_message(self, message):
        """
        Sends a message to the given chat_id

        :param message: Message to send
        :type message: str
        """
        try:
            self.telegram_client.send_message(chat_id=self.chat_id, text=message)
            self.log.info(f'Sending message: {message}')
        except AirflowException as e:
            self.log.exception(f'Error occurred while trying to send a message: {e}')
            raise e

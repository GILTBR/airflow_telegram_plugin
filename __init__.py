from airflow.plugins_manager import AirflowPlugin
from .telegram_hook import TelegramHook
from .telegram_operator import TelegramOperator


class TelegramPlugin(AirflowPlugin):
    name = 'telegram_plugin'
    operators = [TelegramOperator]
    hooks = [TelegramHook]

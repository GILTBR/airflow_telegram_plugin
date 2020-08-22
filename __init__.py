from airflow.plugins_manager import AirflowPlugin

from .hooks.telegram_hook import TelegramHook
from .operators.telegram_operator import TelegramOperator


class TelegramPlugin(AirflowPlugin):
    name = 'telegram_plugin'
    operators = [TelegramOperator]
    hooks = [TelegramHook]

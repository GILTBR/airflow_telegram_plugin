from airflow.plugins_manager import AirflowPlugin

from plugins.airflow_telegram_plugin.hooks.telegram_hook import TelegramHook
from plugins.airflow_telegram_plugin.operators.telegram_operator import TelegramOperator


class TelegramPlugin(AirflowPlugin):
    name = 'telegram_plugin'
    operators = [TelegramOperator]
    hooks = [TelegramHook]

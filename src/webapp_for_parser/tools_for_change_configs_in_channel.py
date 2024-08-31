from src.databases.mongodb import client_mongodb
from typing import Any


def change_configs_in_channel(channel: str, direction: str, data_for_change: Any):
    entry_in_db = client_mongodb.get_config_of_channel(data_for_change['url_of_channel'], direction, with_channel=True)
    for key, value in data_for_change.items():
        if value != '' and key != 'direction' and key != '_auth' and key != 'msg_id' and key != 'with_webview' and key != 'url_of_channel':
            entry_in_db[channel][key] = value
        else:
            continue

    client_mongodb.update_data_in_entity_in_collection_for_parser_configs(direction, channel, entry_in_db)



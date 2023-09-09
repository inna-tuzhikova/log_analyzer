import json
from collections import namedtuple
from pathlib import Path


DEFAULT_CONFIG_DICT = {
    'REPORT_SIZE': 1000,
    'REPORT_DIR': './data/reports',
    'LOG_DIR': './data/logs',
    'MAX_ERROR_RATE': .05,
    'SCRIPT_LOG_PATH': None
}

Config = namedtuple('Config', [
    'report_size', 'report_dir', 'log_dir',
    'max_error_rate', 'script_log_path'
])


def prepare_config(config_path: Path | None = None) -> Config:
    """Cooks config for script

    Args:
        config_path: path to json file with settings. If not specified default
          settings are applied. Omitted settings will be replaced with defaults

    Returns:
        Config file with settings
    """
    result_dict = {}
    if config_path is None:
        user_config_dict = {}
    else:
        with open(config_path, 'r') as f:
            user_config_dict = json.load(f)
        if not isinstance(user_config_dict, dict):
            raise ValueError(
                f'Unsupported config format, expected dict config, '
                f'got {user_config_dict.__class__.__name__}'
            )
    result_dict.update(DEFAULT_CONFIG_DICT)
    result_dict.update(user_config_dict)
    return Config(
        report_size=result_dict['REPORT_SIZE'],
        report_dir=result_dict['REPORT_DIR'],
        log_dir=result_dict['LOG_DIR'],
        max_error_rate=result_dict['MAX_ERROR_RATE'],
        script_log_path=result_dict['SCRIPT_LOG_PATH'],
    )

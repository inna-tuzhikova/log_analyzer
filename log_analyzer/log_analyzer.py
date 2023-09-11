#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Input: nginx log directory
Output: html report with url request time statistics
"""
import logging
from argparse import ArgumentParser
from pathlib import Path

from report import (
    Config,
    build_report,
    find_log,
    get_report_path,
    init_logging,
    prepare_config,
    read_log,
)


def main():
    try:
        config_path = parse_args()
    except FileNotFoundError as e:
        print(f'Exiting program, reason: {e}')
        exit(1)
    try:
        config = prepare_config(config_path)
    except Exception as e:
        print(f'Unable to read `{config_path.absolute()}`: {e}')
        exit(1)

    init_logging(config)
    logger = logging.getLogger(__name__)
    logger.info('Start')

    try:
        analyze_logs(config)
    except:
        logger.exception('Error during analyzing logs...')
        exit(1)
    else:
        logging.getLogger(__name__).info('DONE!')


def parse_args() -> Path | None:
    parser = ArgumentParser('Script analyzing nginx logs')
    parser.add_argument(
        '--config', type=Path, default=Path('data/config.json'),
        help='Path to json file with script options: '
             'REPORT SIZE, REPORT_DIR, LOG_DIR, SCRIPT_LOG_PATH'
    )
    args = parser.parse_args()
    if args.config is not None and not args.config.is_file():
        raise FileNotFoundError(
            f'Cannot find config path: `{args.config.absolute()}`'
        )

    return args.config


def analyze_logs(config: Config) -> None:
    logger = logging.getLogger(__name__)
    log = find_log(config)
    if log is None:
        logger.info('There is no logs to report!')
        return
    report_path = get_report_path(log, config)
    if report_path.is_file():
        logger.info(
            'Report for %s is already built: `%s`',
            log.date, report_path.absolute()
        )
        return
    build_report(read_log(log), report_path, config)
    logger.info('Saved to `%s`', report_path.absolute())


if __name__ == '__main__':
    main()

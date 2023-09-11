import json
import logging
import re
import statistics
from collections import defaultdict, namedtuple
from pathlib import Path
from string import Template
from typing import Generator

from .config import Config
from .fs import get_report_template, save_report

URLStat = namedtuple('URLStat', ['url', 'request_time_sec'])
log_record_fmt = re.compile(
    r'^(?P<remote_addr>.+?) '
    r'(?P<remote_user>.+?) '
    r'(?P<http_x_real_ip>.+?) '
    r'\[(?P<time_local>.+?)\] '
    r'"(?P<request>(?P<method>.+?) (?P<url>.+?) (?P<http>.+?))"'
    r'(?P<status>.+?) '
    r'(?P<body_bytes_sent>.+?) '
    r'"(?P<http_referer>.+?)" '
    r'"(?P<http_user_agent>.+?)" '
    r'"(?P<http_x_forwarded_for>.+?)" '
    r'"(?P<http_X_REQUEST_ID>.+?)" '
    r'"(?P<http_X_RB_USER>.+?)" '
    r'(?P<request_time>.+?)$'
)


logger = logging.getLogger(__name__)


def build_report(
    log_reader: Generator[str, None, None],
    report_path: Path,
    config: Config
) -> None:
    """Builds report based on log file and output options"""
    urls_stat = defaultdict(list)
    error_lines = 0
    total_lines = 0
    for line in log_reader:
        total_lines += 1
        stat = parse_line(line)
        if stat is not None:
            urls_stat[stat.url].append(stat.request_time_sec)
        else:
            error_lines += 1

    error_rate = error_lines / total_lines
    if error_rate > config.max_error_rate:
        logger.info(
            'Too many errors during reading log. '
            'Try to check log format'
        )
        return
    total_requests = sum(
        len(records)
        for url, records in urls_stat.items()
    )
    total_request_time_sec = sum(
        sum(records)
        for url, records in urls_stat.items()
    )
    filtered_stat = sorted(
        urls_stat.items(),
        key=lambda x: sum(x[1]),
        reverse=True
    )[:config.report_size]
    table = prepare_table(
        filtered_stat, total_requests, total_request_time_sec
    )
    report_content = render_table(table)
    save_report(report_content, report_path)


def parse_line(line: str) -> URLStat | None:
    result = None
    match = log_record_fmt.match(line)
    if match is not None:
        result = URLStat(
            url=match.group('url'),
            request_time_sec=float(match.group('request_time'))
        )
    return result


def prepare_table(
    filtered_stat: list[tuple[str, list]],
    total_requests: int,
    total_request_time_sec: float
) -> list[dict]:
    result = []
    for url, time_stat in filtered_stat:
        result.append(dict(
            url=url,
            **prepare_stats(
                time_stat, total_requests, total_request_time_sec
            )
        ))
    return result


def prepare_stats(
    time_stat: list[float],
    total_requests: int,
    total_request_time_sec: float
) -> dict:
    url_requests = len(time_stat)
    url_time = sum(time_stat)
    return dict(
        count=url_requests,
        count_perc=100 * url_requests / total_requests,
        time_sum=url_time,
        time_perc=100 * url_time / total_request_time_sec,
        time_avg=statistics.mean(time_stat),
        time_max=max(time_stat),
        time_med=statistics.median(time_stat),
    )


def render_table(table: list[dict]) -> str:
    content = get_report_template()
    t = Template(content)
    return t.safe_substitute(table_json=json.dumps(table))

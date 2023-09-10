import gzip
import logging
import re
from collections import namedtuple
from datetime import date
from pathlib import Path
from typing import Generator

from .config import Config

Log = namedtuple('Log', ['path', 'date'])
log_name_rexp = re.compile(r'^nginx-access-ui\.log-(?P<date>\d{8})(\.gz)?$')
logger = logging.getLogger(__name__)


def find_log(config: Config) -> Log | None:
    """Finds latest ui log to process

    Args:
        config: settings object. Required option is log directory

    Returns:
        Log instance with meta of found log to process. If no log is found None
          is returned
    """
    last_log = None
    last_date = None

    log_path = Path(config.log_dir)

    if log_path.is_dir():
        for f in log_path.iterdir():
            if f.is_file():
                match = log_name_rexp.match(f.name)
                if match is not None:
                    d = match.group('date')
                    log_date = date(
                        year=int(d[:4]),
                        month=int(d[4:6]),
                        day=int(d[6:])
                    )
                    if last_date is None or log_date > last_date:
                        last_date = log_date
                        last_log = f
    return (
        None
        if last_log is None
        else Log(last_log, last_date)
    )


def get_report_path(log: Log, config: Config) -> Path:
    """Calculates output filename based on log date and output directory"""
    report_dir = Path(config.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f'report-{log.date:%Y.%m.%d}.html'
    return report_path


def read_log(log: Log) -> Generator[list[str], None, None]:
    """Iterator reading log file line by line"""
    opener = gzip.open if log.path.suffix == '.gz' else open
    try:
        with opener(log.path, 'rt') as f:
            for line in f:
                yield line
    except IOError as e:
        # It will be caught further, so no traceback here
        logger.info('Unable to read `%s`', log.path)
        raise e


def save_report(report_content: str, report_path: Path) -> None:
    """Saves report content as a file with specified filename"""
    with open(report_path, 'w') as f:
        f.write(report_content)


def get_report_template() -> str:
    """Returns string representation of html template for cooking report"""
    path = Path(__file__).parent / 'template.html'
    with open(path, 'r') as f:
        content = f.read()
    return content

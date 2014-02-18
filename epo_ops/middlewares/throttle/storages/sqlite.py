# -*- coding: utf-8 -*-

from itertools import cycle
import logging
import os
import re
import sqlite3
from datetime import timedelta

from dateutil.parser import parse

from ....utils import makedirs, now
from .storage import Storage

log = logging.getLogger(__name__)


def convert_timestamp(ts):
    return parse(ts)

sqlite3.register_converter('timestamp', convert_timestamp)


class SQLite(Storage):
    SERVICES = ('images', 'inpadoc', 'other', 'retrieval', 'search')

    def __init__(
        self, db='/var/tmp/python-epo-ops-client/throttle_history.db'
    ):
        makedirs(os.path.dirname(db))
        self.db = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.row_factory = sqlite3.Row
        self.prepare()

    def service_columns(self, include_type=False):
        columns = []
        for service in self.SERVICES:
            columns.extend([
                '{}_status'.format(service),
                '{}_limit'.format(service),
                '{}_retry_after'.format(service)
            ])
        if include_type:
            for i, pair in enumerate(
                zip(columns, cycle(['text', 'integer', 'integer']))
            ):
                columns[i] = '{} {}'.format(*pair)

        return columns

    def prepare(self):
        sql = """\
        CREATE TABLE throttle_history(
            timestamp timestamp primary key,
            system_status text, {}
        )
        """
        try:
            with self.db:
                self.db.execute(
                    sql.format(', '.join(self.service_columns(True)))
                )
        except sqlite3.OperationalError:
            pass

    def prune(self):
        sql = """\
        DELETE FROM throttle_history
        WHERE timestamp < datetime('now', '-1 minute')
        """
        with self.db:
            self.db.execute(sql)

    def parse_throttle(self, throttle):
        re_str = '{}=(\w+):(\d+)'
        status = {'services': {}}
        status['system_status'] = re.search('^(\\w+) \\(', throttle).group(1)
        for service in self.SERVICES:
            match = re.search(re_str.format(service), throttle)
            status['services'][service] = {
                'status': match.group(1),
                'limit': int(match.group(2)),
            }
        return status

    def convert(self, status, retry):
        sql = (
            'INSERT INTO throttle_history(timestamp, system_status, {}) '
            'VALUES ({})'
        ).format(', '.join(self.service_columns()), ', '.join(['?'] * 17))
        values = [now(), status['system_status']]
        for service in self.SERVICES:
            service_status = status['services'][service]['status']
            service_limit = status['services'][service]['limit']
            service_retry = 0
            if service_status.lower() == 'black':
                service_retry = retry
            values.extend([service_status, service_limit, service_retry])
        return sql, values

    def delay_for(self, service):
        "This method is a public interface for a throttle storage class"

        _now = now()
        limit = '{}_limit'.format(service)
        self.prune()
        sql = (
            'SELECT * FROM throttle_history ORDER BY {} limit 1'
        ).format(limit)
        with self.db:
            r = self.db.execute(sql).fetchone()

        if not r:  # If there are no rows
            next_run = _now
        elif r[limit] == 0:
            next_run = r['timestamp'] +\
                timedelta(milliseconds=r['{}_retry_after'.format(service)])
        else:
            next_run = _now + timedelta(seconds=60. / r[limit])
        return (next_run - _now).total_seconds()

    def update(self, headers):
        "This method is a public interface for a throttle storage class"

        self.prune()
        if not 'x-throttling-control' in headers:
            return
        status = self.parse_throttle(headers['x-throttling-control'])
        retry_after = int(headers.get('retry-after', 0))
        sql, values = self.convert(status, retry_after)
        with self.db:
            self.db.execute(sql, values)

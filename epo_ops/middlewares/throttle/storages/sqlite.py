# -*- coding: utf-8 -*-

from __future__ import division

import logging
import os
import re
import sqlite3
from datetime import timedelta
from itertools import cycle

from dateutil.parser import parse

from ....utils import makedirs, now
from .storage import Storage

log = logging.getLogger(__name__)


def convert_timestamp(ts):
    return parse(ts)


sqlite3.register_converter("timestamp", convert_timestamp)

# FIXME: S108 Probable insecure usage of temporary file or directory: "/var/tmp/python-epo-ops-client/cache.dbm"
DEFAULT_DB_PATH = "/var/tmp/python-epo-ops-client/throttle_history.db"  # noqa: S108


class SQLite(Storage):
    SERVICES = ("images", "inpadoc", "other", "retrieval", "search")

    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = db_path
        makedirs(os.path.dirname(db_path))
        self.db = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.row_factory = sqlite3.Row
        self.prepare()

    def service_columns(self, include_type=False):
        columns = []
        for service in self.SERVICES:
            columns.extend(
                [
                    "{0}_status".format(service),
                    "{0}_limit".format(service),
                    "{0}_retry_after".format(service),
                ]
            )
        if include_type:
            for i, pair in enumerate(
                zip(columns, cycle(["text", "integer", "integer"]))
            ):
                columns[i] = "{0} {1}".format(*pair)

        return columns

    def prepare(self):
        sql = """\
        CREATE TABLE throttle_history(
            timestamp timestamp primary key,
            system_status text, {0}
        )
        """
        try:
            with self.db:
                self.db.execute(sql.format(", ".join(self.service_columns(True))))
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
        re_str = r"{0}=(\w+):(\d+)"
        status = {"services": {}}
        status["system_status"] = re.search("^(\\w+) \\(", throttle).group(1)
        for service in self.SERVICES:
            match = re.search(re_str.format(service), throttle)
            status["services"][service] = {
                "status": match.group(1),
                "limit": int(match.group(2)),
            }
        return status

    def convert(self, status, retry):
        sql = (
            "INSERT INTO throttle_history(timestamp, system_status, {0}) "
            "VALUES ({1})"
        ).format(", ".join(self.service_columns()), ", ".join(["?"] * 17))
        values = [now(), status["system_status"]]
        for service in self.SERVICES:
            service_status = status["services"][service]["status"]
            service_limit = status["services"][service]["limit"]
            service_retry = 0
            if service_status.lower() == "black":
                service_retry = retry
            values.extend([service_status, service_limit, service_retry])
        return sql, values

    def delay_for(self, service):
        "This method is a public interface for a throttle storage class"

        _now = now()
        limit = "{0}_limit".format(service)
        self.prune()
        sql = ("SELECT * FROM throttle_history ORDER BY {0} limit 1").format(limit)
        with self.db:
            r = self.db.execute(sql).fetchone()

        if not r:  # If there are no rows
            next_run = _now
        elif r[limit] == 0:
            next_run = r["timestamp"] + timedelta(
                milliseconds=r["{0}_retry_after".format(service)]
            )
        else:
            next_run = _now + timedelta(seconds=60.0 / r[limit])

        if next_run < _now:
            return 0.0
        else:
            td = next_run - _now
            ts = td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6
            return ts / 10**6

    def update(self, headers):
        "This method is a public interface for a throttle storage class"

        self.prune()
        if "x-throttling-control" not in headers:
            return
        status = self.parse_throttle(headers["x-throttling-control"])
        retry_after = int(headers.get("retry-after", 0))
        sql, values = self.convert(status, retry_after)
        with self.db:
            self.db.execute(sql, values)

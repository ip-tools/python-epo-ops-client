import json


def status_generator(timestamp, status, limit, retry_after=None):
    return {
        'timestamp': timestamp,
        'status': status,
        'limit': limit,
        'retry_after': retry_after or 0,
    }


def status_dict(service, datetimes, service_status):
    statuses = []
    for dt, status in zip(datetimes, service_status):
        statuses.append(status_generator(dt, *status))
    return {
        service: statuses
    }


class ServiceHistory(object):
    def __init__(self, service, datetimes, service_status):
        self.service = service
        self.datetimes = datetimes
        self.service_status = service_status

    def as_datetime(self):
        return status_dict(self.service, self.datetimes, self.service_status)

    def as_isoformat(self):
        return status_dict(
            self.service, [dt.isoformat() for dt in self.datetimes],
            self.service_status
        )


class ThrottleHistory(object):
    def __init__(self, *service_statuses):
        self.service_statuses = service_statuses

    @property
    def base(self):
        return {
            'system_status': 'idle',  # idle, busy, overloaded
            'services': {},
        }

    def as_dict(self):
        ts = self.base
        for status in self.service_statuses:
            ts['services'].update(status.as_datetime())
        return ts

    def as_json(self):
        ts = self.base
        for status in self.service_statuses:
            ts['services'].update(status.as_isoformat())
        return json.dumps(ts, indent=2)

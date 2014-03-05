class ServiceSnapshot(object):
    def __init__(self, service, status, limit):
        self.service = service
        self.status = status
        self.limit = limit

    def as_header(self):
        return '{0}={1}:{2}'.format(self.service, self.status, self.limit)

    def as_dict(self):
        return {
            self.service: {
                'status': self.status,
                'limit': self.limit,
            }
        }


class ThrottleSnapshot(object):
    def __init__(self, system_status, service_statuses):
        self.system_status = system_status
        self.service_statuses = service_statuses

    @property
    def base(self):
        return {
            'system_status': 'idle',  # idle, busy, overloaded
            'services': {},
        }

    def as_header(self):
        services = []
        for status in self.service_statuses:
            services.append(status.as_header())
        return '{0} ({1})'.format(self.system_status, ', '.join(services))

    def as_dict(self):
        ts = {
            'system_status': self.system_status,
            'services': {},
        }
        ts = self.base
        for status in self.service_statuses:
            ts['services'].update(status.as_dict())
        return ts

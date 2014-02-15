class ServiceSnapshot(object):
    def __init__(self, service, service_status):
        self.service = service
        self.service_status = service_status

    def as_header(self):
        return '{}={}:{}'.format(self.service, *self.service_status)

    def as_dict(self):
        return {
            self.service: {
                'status': self.service_status[0],
                'limit': self.service_status[1],
            }
        }


class ThrottleSnapshot(object):
    def __init__(self, system_status, *service_statuses):
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
        return '{} ({})'.format(self.system_status, ', '.join(services))

    def as_dict(self):
        ts = {
            'system_status': self.system_status,
            'services': {},
        }
        ts = self.base
        for status in self.service_statuses:
            ts['services'].update(status.as_dict())
        return ts

import logging

log = logging.getLogger(__name__)


class Client(object):
    def __init__(self, accept_type='xml'):
        self.accept_type = accept_type


class RegisteredClient(Client):
    def __init__(self, key, secret, accept_type='xml'):
        super(RegisteredClient, self).__init__(accept_type)
        self.key = key
        self.secret = key

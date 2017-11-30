import socket as sock_module
import base


class client(base.base):
    def __init__(self, config={}):
        super(client, self)


def run(config):
    print(config)
    c = client(config)
    del c


if __name__ == "__main__":
    run(base.test_config)

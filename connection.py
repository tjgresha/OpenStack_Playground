import openstack
from openstack.config import loader


openstack.enable_logging(True, stream=sys.stdout)


class Opts:
    def __init__(self, cloud_name='openstack', debug=False):
        self.cloud = cloud_name
        self.debug = debug
        # Use identity v3 API for examples.
        self.identity_api_version = '3'

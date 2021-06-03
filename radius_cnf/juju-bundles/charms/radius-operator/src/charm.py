#!/usr/bin/env python3
# Copyright 2021 Tolga Golelcin
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)


class RadiusCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.config_changed, self.configure_pod)
        self.framework.observe(self.on.leader_elected, self.configure_pod)
        self.framework.observe(self.on.adduser_action, self.adduser)

    def configure_pod(self, _):
        self.model.pod.set_spec(
            {
                "version": 3,
                "containers": [  # list of containers for the pod
                    {
                        "name": "radius",  # container name
                        "image": "2stacks/freeradius",  # image for the container
                        "ports": [  # ports exposed by the container
                            {
                                "name": "udp1",
                                "containerPort": 1812,
                                "protocol": "UDP",
                            },
                            {
                                "name": "udp2",
                                "containerPort": 1813,
                                "protocol": "UDP",
                            }
                        ],
                        "envConfig": {  # Environment variables that wil be passed to the container
                            "DB_HOST": "mysql",
                            "RAD_DEBUG": "yes",
                        },
                    }
                ],
            }
        )
        self.unit.status = ActiveStatus()

    def adduser(self, event):
        username = event.params["username"]
        password = event.params["password"]
        try:
            cmd="echo '{} Cleartext-Password := \"{}\"' >> /etc/raddb/users".format(username, password)
            subprocess.run([cmd])
            event.set_results({
            "output": f"User {username} created successfully"
            })
        except Exception as e:
            event.fail(f"Touch action failed with the following exception: {e}")


if __name__ == "__main__":
    main(RadiusCharm)

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


class MysqlCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.config_changed, self.configure_pod)
        self.framework.observe(self.on.leader_elected, self.configure_pod)

    def configure_pod(self, _):
        self.model.pod.set_spec(
            {
                "version": 3,
                "containers": [  # list of containers for the pod
                    {
                        "name": "mysql",  # container name
                        "image": "mysql",  # image for the container
                        "ports": [  # ports exposed by the container
                            {
                                "name": "tcp1",
                                "containerPort": 3306,
                                "protocol": "TCP",
                            },
                        ],
                        "envConfig": {  # Environment variables that wil be passed to the container
                            "MYSQL_ROOT_PASSWORD": "radius",
                            "MYSQL_USER": "radius",
                            "MYSQL_PASSWORD": "radpass",
                            "MYSQL_DATABASE": "radius",
                        },
                    }
                ],
            }
        )
        self.unit.status = ActiveStatus()

if __name__ == "__main__":
    main(MysqlCharm)

# -*- coding: utf-8 -*-

# Copyright 2015 LIP - INDIGO-DataCloud
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from ooi.api import base
import ooi.api.helpers
from ooi import exception
from ooi.occi.core import collection
from ooi.occi.infrastructure import compute
from ooi.occi.infrastructure import securitygroup
# from ooi.occi.infrastructure import security_group_link
from ooi.occi import validator as occi_validator


class Controller(base.Controller):
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        self.os_helper = ooi.api.helpers.OpenStackHelper(
            self.app,
            self.openstack_version
        )

    def index(self, req):
        raise exception.NotImplemented()

    def show(self, req, id):
        raise exception.NotImplemented()

    def create(self, req, body):
        raise exception.NotImplemented()

    def delete(self, req, id):
        raise exception.NotImplemented()

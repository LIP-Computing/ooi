# -*- coding: utf-8 -*-

# Copyright 2015 LIP - Lisbon
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

from ooi.tests import base
from ooi.tests.integration.keystone import session


class TestIntegration(base.TestController):

    def setUp(self):
        super(TestIntegration, self).setUp()
        self.project_id = "1217d4751d91448bac885955cf7cb7d7"
        self.public_network = "d34b55b0-6098-4411-8142-a35f48d623f6"
        self.new_network_name = "networkTEST_OCCINET"
        self.session = session.KeySession().create_keystone("demo", "all-in16", self.project_id)
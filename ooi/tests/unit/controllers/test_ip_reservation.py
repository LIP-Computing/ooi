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

import mock

from ooi.api import helpers
from ooi.api import ip_reservation as ip_reservation_control
from ooi import exception
from ooi.occi.infrastructure import ip_reservation
from ooi.tests import base
from ooi.tests import fakes


class TestIPReservationController(base.TestController):
    def setUp(self):
        super(TestIPReservationController, self).setUp()
        self.controller = ip_reservation_control.Controller(
            mock.MagicMock(), None
        )

    @mock.patch.object(helpers.OpenStackHelper, "get_floating_ips")
    def test_index_empty(self, m_iplist):
        tenant = fakes.tenants["foo"]
        floating_list = fakes.floating_ips[tenant["id"]]
        m_iplist.return_value = floating_list
        result = self.controller.index(None)
        expected = self.controller._get_ipreservation_resources(floating_list)
        self.assertEqual(expected, result.resources)
        self.assertEqual([], result.resources)
        m_iplist.assert_called_with(None)

    @mock.patch.object(helpers.OpenStackHelper, "get_floating_ips")
    def test_index(self, m_iplist):
        tenant = fakes.tenants["baz"]
        floating_list = fakes.floating_ips[tenant["id"]]
        m_iplist.return_value = floating_list
        result = self.controller.index(None)
        expected = self.controller._get_ipreservation_resources(floating_list)
        self.assertEqual(expected, result.resources)
        m_iplist.assert_called_with(None)

    @mock.patch.object(helpers.OpenStackHelper, "get_floating_ip")
    def test_show(self, m_ip):
        tenant = fakes.tenants["baz"]
        floating_ip = fakes.floating_ips[tenant["id"]][0]
        m_ip.return_value = floating_ip
        result = self.controller.show(None, floating_ip["id"])
        expected = self.controller._get_ipreservation_resources(
            [floating_ip])[0]
        self.assertIsInstance(result, ip_reservation.IPReservation)
        self.assertEqual(expected, result)
        m_ip.assert_called_with(None, floating_ip["id"])

    def test_delete(self):
        tenant = fakes.tenants["baz"]
        floating_ip = fakes.floating_ips[tenant["id"]][0]
        self.assertRaises(exception.NotImplemented,
                          self.controller.delete,
                          None, floating_ip["id"])

    def test_create(self):
        self.assertRaises(exception.NotImplemented,
                          self.controller.create,
                          None)
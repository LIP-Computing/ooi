# Copyright 2016 LIP - Lisbon
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
import webob

from ooi.tests.tests_integration.integration import  TestIntegration

from ooi import exception
from ooi.wsgi import Request
from ooi.api import ip_reservation as ip_reservation_controller
from ooi.api import query
from ooi.occi.infrastructure import ip_reservation
from ooi.tests.tests_integration.integration.keystone.session import KeySession
from ooi.tests import fakes_network as fakes


class TestIntegrationIPReservation(TestIntegration):

    def setUp(self):
        super(TestIntegrationIPReservation, self).setUp()
        self.req = Request(
            KeySession().create_request_nova(self.session, path="/",
                                        environ={},
                                        headers={
                                            "X_PROJECT_ID": self.project_id
                                        }).environ)

        self.controller = ip_reservation_controller.Controller(
            app=None,openstack_version="/v2.1"
        )

    def test_list(self):
        list = self.controller.index(self.req)
        self.assertIsInstance(list.resources[0], ip_reservation.IPReservation)
        self.assertEqual(2, list.resources.__len__())

    def test_show(self):
        reservation_id = '705f8740-5bcc-4a3b-9375-1ef4718d5e88'
        result = self.controller.show(self.req, reservation_id)
        self.assertIsInstance(result, ip_reservation.IPReservation)
        self.assertEqual("external-net", result.title)

    def test_query(self):
        query_controller = query.Controller(
            app=None,openstack_version="/v2.1"
        )
        list = query_controller.index(self.req)
        self.assertIsInstance(list[list.__len__()-1],  ip_reservation.IPReservation)
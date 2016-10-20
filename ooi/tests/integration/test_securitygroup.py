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

from ooi.tests.integration import  TestIntegration

from ooi import exception
from ooi.wsgi import Request
from ooi.api import securitygroup as security_group_controller
from ooi.api import query
from ooi.occi.infrastructure import securitygroup
from ooi.openstack import helpers as os_helpers
from ooi.tests.integration.keystone.session import KeySession
from ooi.tests import fakes_network
from ooi.tests import fakes as fakes_nova
from ooi import utils
from ooi.tests.integration.keystone import session


class TestIntegrationSecGroups(TestIntegration):

    def setUp(self):
        super(TestIntegrationSecGroups, self).setUp()
        self.req = Request(
            KeySession().create_request_ssl(self.session, path="/",
                                        environ={},
                                        headers={
                                            "X_PROJECT_ID": self.project_id
                                        }).environ)

        self.controller = security_group_controller.Controller(
            app=None, neutron_ooi_endpoint="https://192.92.149.119:9696/v2.0"
        )

    def test_list(self):
        list = self.controller.index(self.req)
        self.assertIsInstance(list.resources[0], securitygroup.SecurityGroup)

    def test_show(self):
        htts_sec = "b86534fa-2435-4d6c-b0d7-ad77f24411e0"
        resources = self.controller.show(self.req, htts_sec)
        self.assertIsInstance(resources, securitygroup.SecurityGroup)

    # def test_create_securitygroup(self):
    #     tenant_id = fakes.tenants["foo"]["id"]
    #     sec_group = os_helpers.build_security_group_from_neutron(
    #         fakes.security_groups[tenant_id]
    #     )[0]
    #     params = {"occi.core.title": "testgroup",
    #               "occi.securitygroup.rules": sec_group["rules"]
    #               }
    #     categories = {securitygroup.SecurityGroup.kind}
    #     occi_headers = fakes.create_header_occi(params, categories)
    #     self.req.headers.update(occi_headers)
    #     ret = self.controller.create(self.req, params)
    #     expected = self.controller._get_security_group_resources([sec_group])
    #
    # def test_delete(self):
    #     htts_sec = 'e67864bf-e8d3-4512-a7ee-cff8eba8ff3b'
    #     resources = self.controller.delete(self.req, htts_sec)
    #     self.assertEqual([], resources)


class TestIntegrationSecGroupsNova(TestIntegration):

    def setUp(self):
        super(TestIntegrationSecGroupsNova, self).setUp()
        self.req = Request(
            KeySession().create_request_nova_ssl(self.session, path="/",
                                        environ={},
                                        headers={
                                            "X_PROJECT_ID": self.project_id
                                        }).environ)

        self.controller = security_group_controller.Controller(
            app=None, openstack_version="/v2.1"
        )

    def test_list(self):
        list = self.controller.index(self.req)
        self.assertIsInstance(list.resources[0], securitygroup.SecurityGroup)

    def test_show(self):
        htts_sec = "5cbb5205-035b-4c51-8eb8-0800f614614c"
        resources = self.controller.show(self.req, htts_sec)
        self.assertIsInstance(resources, securitygroup.SecurityGroup)

    # def test_create_securitygroup(self):
    #     tenant_id = fakes_nova.tenants["foo"]["id"]
    #     sec_group = os_helpers.build_security_group_from_nova(
    #         fakes_nova.security_groups[tenant_id]
    #     )[0]
    #     params = {"occi.core.title": "testgroup2",
    #               "occi.core.summary": "group two for testing",
    #               "occi.securitygroup.rules": sec_group["rules"]
    #               }
    #     categories = {securitygroup.SecurityGroup.kind}
    #     occi_headers = fakes_network.create_header_occi(params, categories)
    #     self.req.headers.update(occi_headers)
    #     ret = self.controller.create(self.req, params)
    #     expected = self.controller._get_security_group_resources([sec_group])
    #
    # def test_delete(self):
    #     htts_sec = '778ba860-df55-4b2d-9e93-9099cfaf01cf'
    #     resources = self.controller.delete(self.req, htts_sec)
    #     self.assertEqual([], resources)

# class TestMiddleware(TestIntegration):
#     def setUp(self):
#         super(TestMiddleware, self).setUp()
#         endpoint = "http://%s/9696/v2.0" % session.IP_SERVER
#         self.app = wsgi.OCCIMiddleware(None, neutron_ooi_endpoint=endpoint)
#
#     def test_list_links(self):
#         headers = {
#             #'Category': 'network; scheme="http://schema#";class="kind";',
#             "X_PROJECT_ID": self.project_id,
#         }
#         req = KeySession().create_request(self.session, headers=headers, path="/networklink")
#         result = req.get_response(self.app)
#         self.assertEqual(200, result.status_code)
#         self.assertIsNot("", result.text)
    #
    # def test_show(self):
    #     reservation_id = '705f8740-5bcc-4a3b-9375-1ef4718d5e88'
    #     result = self.controller.show(self.req, reservation_id)
    #     self.assertIsInstance(result, ip_reservation.IPReservation)
    #     self.assertEqual("external-net", result.title)
    #
    # def test_query(self):
    #     query_controller = query.Controller(
    #         app=None,openstack_version="/v2.1"
    #     )
    #     list = query_controller.index(self.req)
    #     self.assertIsInstance(list[list.__len__()-1],  ip_reservation.IPReservation)
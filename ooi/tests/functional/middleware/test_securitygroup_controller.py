# -*- coding: utf-8 -*-

# Copyright 2015 Spanish National Research Council
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

from oslo_config import cfg
import webob

from ooi.api import helpers
from ooi.openstack import helpers as os_helpers
from ooi.tests import fakes_network as fakes
from ooi.tests.functional.middleware import test_middleware
from ooi import utils
from ooi import wsgi


class TestNetSecGroupController(test_middleware.TestMiddleware):
    """Test OCCI security group controller."""

    def setUp(self):
        super(TestNetSecGroupController, self).setUp()
        self.schema = 'http://schemas.ogf.org/occi/infrastructure#securitygroup'
        self.application_url = fakes.application_url
        neutron_ooi_endpoint = "foo"

        def mock_endpoint(self, bar):
            if bar == "neutron_ooi_endpoint":
                return neutron_ooi_endpoint

        with mock.patch.object(cfg.ConfigOpts, "__getattr__",
                               side_effect=mock_endpoint,
                               autospec=True):
            self.app = wsgi.OCCIMiddleware(None)

    def assertExpectedResult(self, expected, result):
        expected = ["%s: %s" % e for e in expected]
        # NOTE(aloga): the order of the result does not matter
        results = str(result.text).splitlines()
        self.assertItemsEqual(expected, results)

    @mock.patch.object(helpers.BaseHelper, "_get_req")
    def test_list_sec_empty(self, m):
        tenant = fakes.tenants["bar"]
        out = fakes.create_fake_json_resp(
            {"security_group": fakes.security_groups[tenant['id']]}, 200)
        m.return_value.get_response.return_value = out

        req = self._build_req(path="/securitygroup",
                              tenant_id='X', method="GET")
        resp = req.get_response(self.app)

        self.assertEqual(204, resp.status_code)
        expected_result = ""
        self.assertExpectedResult(expected_result, resp)
        self.assertDefaults(resp)

    @mock.patch.object(helpers.BaseHelper, "_get_req")
    def test_list_securitygroup(self, m):
        tenant = fakes.tenants["foo"]
        out = fakes.create_fake_json_resp(
            {"security_groups": fakes.security_groups[tenant['id']]}, 200)
        m.return_value.get_response.return_value = out
        req = self._build_req(path="/securitygroup",
                              tenant_id='X', method="GET")
        resp = req.get_response(self.app)

        self.assertEqual(200, resp.status_code)
        expected = []
        for s in fakes.security_groups[tenant["id"]]:
            expected.append(
                ("X-OCCI-Location",
                 utils.join_url(self.application_url + "/",
                                "securitygroup/%s" % s["id"]))
            )
        self.assertDefaults(resp)
        self.assertExpectedResult(expected, resp)

    @mock.patch.object(helpers.BaseHelper, "_get_req")
    def test_show_securitygroup(self, m):
        tenant = fakes.tenants["foo"]
        for s in fakes.security_groups[tenant["id"]]:
            s_out = fakes.create_fake_json_resp(
                {"security_group": s}, 200)
            mock_sec = mock.Mock(webob.Request)
            mock_sec.get_response.return_value = s_out
            m.side_effect = [mock_sec]

            req = self._build_req(path="/securitygroup/%s" % s["id"],
                                  tenant_id='X',
                                  method="GET")
            resp = req.get_response(self.app)
            expected = fakes.build_occi_securitygroup(s)
            self.assertEqual(200, resp.status_code)
            self.assertDefaults(resp)
            self.assertExpectedResult(expected, resp)

    @mock.patch.object(helpers.BaseHelper, "_get_req")
    def test_delete_securitygroup(self, m):
        tenant = fakes.tenants["foo"]
        empty_out = fakes.create_fake_json_resp([], 204)
        mock_empty = mock.Mock(webob.Request)
        mock_empty.get_response.return_value = empty_out
        for s in fakes.security_groups[tenant["id"]]:
            m.side_effect = [mock_empty]
            m.return_value = fakes.create_fake_json_resp(
                {"security_group": s}, 200)
            req = self._build_req(path="/securitygroup/%s" % s["id"],
                                  tenant_id='X',
                                  method="DELETE")
            resp = req.get_response(self.app)
            self.assertEqual(204, resp.status_code)
            self.assertDefaults(resp)

    @mock.patch.object(helpers.BaseHelper, "_get_req")
    def test_create_securitygroup(self, m):
        array_mocks = []
        tenant = fakes.tenants["foo"]
        fake_sc = fakes.security_groups[tenant['id']][0]
        sc_out = fakes.create_fake_json_resp(
            {"security_group": fake_sc}, 200)

        mock_group = mock.Mock(webob.Request)
        mock_group.get_response.return_value = sc_out
        array_mocks.append(mock_group)
        for r in fake_sc["security_group_rules"]:
            rule_out = fakes.create_fake_json_resp(
                {"security_group_rule": r}, 200)
            mock_rule = mock.Mock(webob.Request)
            mock_rule.get_response.return_value = rule_out
            array_mocks.append(mock_rule)
        m.side_effect = array_mocks
        name = fake_sc["name"]
        sc_id = fake_sc["id"]
        fake_occi_rules = os_helpers.build_security_group_from_neutron(
            [fake_sc]
        )
        rules = str(fake_occi_rules[0]["rules"])
        headers = {
            'Category': 'securitygroup;'
                        ' scheme='
                        '"http://schemas.ogf.org/occi/infrastructure#";'
                        'class="kind",',
            'X-OCCI-Attribute': '"occi.core.title"="%s",'
                                '"occi.securitygroup.rules"="%s"' %
                                (name, rules)
        }
        req = self._build_req(path="/securitygroup",
                              tenant_id='X',
                              method="POST",
                              headers=headers)

        resp = req.get_response(self.app)
        self.assertEqual(200, resp.status_code)
        expected = [("X-OCCI-Location",
                     utils.join_url(self.application_url + "/",
                                    "securitygroup/%s" % sc_id))]
        self.assertExpectedResult(expected, resp)

class NetworkNovaControllerTextPlain(test_middleware.TestMiddlewareTextPlain,
                                     TestNetSecGroupController):
    """Test OCCI network controller with Accept: text/plain."""


class NetworkNovaControllerTextOcci(test_middleware.TestMiddlewareTextOcci,
                                    TestNetSecGroupController):
    """Test OCCI network controller with Accept: text/occi."""

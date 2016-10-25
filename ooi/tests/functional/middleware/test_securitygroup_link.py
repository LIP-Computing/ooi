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

import uuid

from ooi.api import helpers
from ooi.tests import fakes
from ooi.tests.functional.middleware import test_middleware
from ooi import utils


class TestSecurityGroupLinkController(test_middleware.TestMiddleware):
    """Test OCCI security link controller."""

    def setUp(self):
        super(TestSecurityGroupLinkController, self).setUp()
        self.application_url = fakes.application_url
        self.app = self.get_app()

    def test_list_secgroup_links(self):
        tenant_id = fakes.tenants['foo']["id"]
        for url in ("/securitygrouplink/", "/securitygrouplink"):
            req = self._build_req(url, tenant_id, method="GET")
            resp = req.get_response(self.app)
            self.assertEqual(200, resp.status_code)
            expected = []
            for s in fakes.servers[tenant_id]:
                for sg in fakes.security_groups[tenant_id]:
                    expected.append(
                        ("X-OCCI-Location",
                         utils.join_url(self.application_url + "/",
                                        "securitygrouplink/%s_%s"
                                        % (
                                            s["id"], sg["id"])
                                        )
                         )
                    )
        self.assertDefaults(resp)
        self.assertExpectedResult(expected, resp)

    def test_secgroup_show(self):
        tenant_id = fakes.tenants['foo']["id"]
        security_groups = fakes.security_groups[tenant_id]
        for s in fakes.servers[tenant_id]:
            server_id = s["id"]
            for sg in security_groups:
                source = utils.join_url(self.application_url + "/",
                                        "compute/%s" % server_id)
                target = utils.join_url(
                    self.application_url + "/",
                    "securitygroup/%s" % sg["id"])
                link_id = '_'.join([server_id,
                                    sg["id"]]
                                   )
                req = self._build_req("/securitygrouplink/%s" % link_id,
                                      tenant_id, method="GET")
                resp = req.get_response(self.app)
                self.assertContentType(resp)
                self.assertResultIncludesLinkAttr(link_id, source, target,
                                                  resp)

    def test_create_link(self):
        tenant_id = fakes.tenants['foo']["id"]
        server_id = uuid.uuid4().hex
        sg_id = fakes.security_groups[tenant_id][0]["id"]

        server_url = utils.join_url(self.application_url + "/",
                                    "compute/%s" % server_id)
        sg_url = utils.join_url(self.application_url + "/",
                                 "securitygroup/%s" % sg_id)
        pool_name = 'pool'
        headers = {
            'Category': ('securitygrouplink;'
                         'scheme="http://schemas.ogf.org/occi/'
                         'infrastructure#";'
                         'class="kind",'),
            'X-OCCI-Attribute': ('occi.core.source="%s", '
                                 'occi.core.target="%s"'
                                 ) % (server_url, sg_url)
        }
        req = self._build_req("/securitygrouplink", tenant_id, method="POST",
                              headers=headers)
        resp = req.get_response(self.app)

        link_id = '_'.join([server_id, sg_id])
        expected = [("X-OCCI-Location",
                     utils.join_url(self.application_url + "/",
                                    "securitygrouplink/%s" % link_id))]
        self.assertEqual(200, resp.status_code)
        self.assertExpectedResult(expected, resp)
        self.assertDefaults(resp)
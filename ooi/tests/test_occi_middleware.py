# -*- coding: utf-8 -*-

# Copyright 2015 Spanish National Research Council
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

from ooi.tests import base
import ooi.tests.test_wsgi
from ooi import wsgi

fake_app = ooi.tests.test_wsgi.fake_app


class TestMiddleware(base.TestCase):
    """OCCI middleware test without Accept header.

    According to the OCCI HTTP rendering, no Accept header
    means text/plain.
    """

    def setUp(self):
        super(TestMiddleware, self).setUp()

        self.app = wsgi.OCCIMiddleware(fake_app)
        self.accept = None

    def assertContentType(self, result):
        expected = self.accept or "text/plain"
        self.assertEqual(expected, result.content_type)

    def assertExpectedResult(self, expected, result):
        expected = ["%s: %s" % e for e in expected]
        self.assertEqual("\n".join(expected), result.text)

    def _build_req(self, path, **kwargs):
        if self.accept is not None:
            kwargs["accept"] = self.accept
        return webob.Request.blank(path,
                                   **kwargs)

    def test_404(self):
        result = self._build_req("/").get_response(self.app)
        self.assertEqual(404, result.status_code)


class TestMiddlewareTextPlain(TestMiddleware):
    """OCCI middleware test with Accept: text/plain."""

    def setUp(self):
        super(TestMiddlewareTextPlain, self).setUp()

        self.app = wsgi.OCCIMiddleware(fake_app)
        self.accept = "text/plain"

    def test_correct_accept(self):
        self.assertEqual("text/plain", self.accept)


class TestMiddlewareTextOcci(TestMiddleware):
    """OCCI middleware text with Accept: text/occi."""

    def setUp(self):
        super(TestMiddlewareTextOcci, self).setUp()

        self.app = wsgi.OCCIMiddleware(fake_app)
        self.accept = "text/occi"

    def assertExpectedResult(self, expected, result):
        for hdr, val in expected:
            self.assertIn(val, result.headers.getall(hdr))

    def test_correct_accept(self):
        self.assertEqual("text/occi", self.accept)


class TestQueryController(TestMiddleware):
    """Test OCCI query controller."""

    def test_query(self):
        result = self._build_req("/-/").get_response(self.app)

        expected_result = [
            ('Category', 'start; scheme="http://schemas.ogf.org/occi/infrastructure/compute/action"; class="action"'),  # noqa
            ('Category', 'stop; scheme="http://schemas.ogf.org/occi/infrastructure/compute/action"; class="action"'),  # noqa
            ('Category', 'restart; scheme="http://schemas.ogf.org/occi/infrastructure/compute/action"; class="action"'),  # noqa
            ('Category', 'suspend; scheme="http://schemas.ogf.org/occi/infrastructure/compute/action"; class="action"'),  # noqa
        ]

        self.assertContentType(result)
        self.assertExpectedResult(expected_result, result)
        self.assertEqual(200, result.status_code)


class QueryControllerTextPlain(TestMiddlewareTextPlain, TestQueryController):
    """Test OCCI query controller with Accept: text/plain."""


class QueryControllerTextOcci(TestMiddlewareTextOcci, TestQueryController):
    """Test OCCI query controller with Accept: text/cci."""
